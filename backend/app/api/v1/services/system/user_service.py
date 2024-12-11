# -*- coding: utf-8 -*-

import io
from typing import Any, Dict, List
from fastapi import Request, UploadFile
import pandas as pd

from app.core.exceptions import CustomException
from app.core.hash_bcrpy import PwdUtil
from app.api.v1.cruds.system.position_crud import PositionCRUD
from app.api.v1.cruds.system.role_crud import RoleCRUD
from app.api.v1.schemas.common.common_schema import UploadResponseSchema
from app.core.base_schema import BatchSetAvailable
from app.utils.excel_util import ExcelUtil
from app.utils.upload_util import UploadUtil
from app.api.v1.cruds.system.user_crud import UserCRUD
from app.api.v1.cruds.system.menu_crud import MenuCRUD
from app.api.v1.cruds.system.dept_crud import DeptCRUD
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.menu_schema import MenuOutSchema
from app.api.v1.schemas.system.user_schema import (
    CurrentUserUpdateSchema,
    UserOutSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserChangePasswordSchema,
    UserRegisterSchema,
    UserForgetPasswordSchema
)
from app.api.v1.params.system.user_param import UserQueryParams


class UserService:
    """用户模块服务层"""

    @classmethod
    async def get_detail_by_id(cls, auth: AuthSchema, id: int) -> Dict:
        """获取用户详情"""
        user = await UserCRUD(auth).get_user_by_id(id=id)
        if not user:
            raise CustomException(msg="用户不存在")
        
        # 如果用户绑定了部门,则获取部门名称
        if user.dept_id:
            dept = await DeptCRUD(auth).get_dept_by_id(id=user.dept_id)
            user.dept_name = dept.name if dept else None
        else:
            user.dept_name = None
            
        return UserOutSchema.model_validate(user).model_dump()

    @classmethod
    async def get_user_list(cls, search: UserQueryParams, order_by: List[Dict], auth: AuthSchema) -> List[Dict]:
        user_list = await UserCRUD(auth).get_user_list(search=search.__dict__, order_by=order_by)
        user_dict_list = []
        for user in user_list:
            if user.dept_id:
                dept = await DeptCRUD(auth).get_dept_by_id(id=user.dept_id)
                user.dept_name = dept.name if dept else None
            else:
                user.dept_name = None
            user_dict = UserOutSchema.model_validate(user).model_dump()
            user_dict_list.append(user_dict)

        return user_dict_list

    @classmethod
    async def create_user(cls, data: UserCreateSchema, auth: AuthSchema) -> Dict:
        # 检查用户名是否存在
        user = await UserCRUD(auth).get_user_by_username(username=data.username)
        if user:
            raise CustomException(msg='已存在相同用户名称的账号')

        # 检查部门是否存在
        if data.dept_id:
            dept = await DeptCRUD(auth).get_dept_by_id(id=data.dept_id)
            if not dept:
                raise CustomException(msg='部门不存在')

        # 创建用户
        data.password = PwdUtil.set_password_hash(password=data.password)
        user_dict = data.model_dump(exclude_unset=True, exclude={"role_ids", "position_ids"})
        new_user = await UserCRUD(auth).create(data=user_dict)

        # 设置角色和岗位
        if data.role_ids and len(data.role_ids) > 0:
            await UserCRUD(auth).set_user_roles(user_ids=[new_user.id], role_ids=data.role_ids)
        if data.position_ids and len(data.position_ids) > 0:
            await UserCRUD(auth).set_user_positions(user_ids=[new_user.id], position_ids=data.position_ids)

        new_user_dict = UserOutSchema.model_validate(new_user).model_dump()
        return new_user_dict

    @classmethod
    async def update_user(cls, data: UserUpdateSchema, auth: AuthSchema) -> Dict:
        # 检查用户是否存在
        user = await UserCRUD(auth).get_user_by_id(id=data.id)
        if not user:
            raise CustomException(msg='用户不存在')

        # 检查用户名是否重复
        exist_user = await UserCRUD(auth).get_user_by_username(username=data.username)
        if exist_user and exist_user.id != data.id:
            raise CustomException(msg='已存在相同的用户名')

        # 检查部门是否存在且可用
        if data.dept_id:
            dept = await DeptCRUD(auth).get_dept_by_id(id=data.dept_id)
            if not dept:
                raise CustomException(msg='部门不存在')
            if not dept.available:
                raise CustomException(msg='部门已被禁用')

        # 更新密码
        if data.password:
            data.password = PwdUtil.set_password_hash(password=data.password)

        # 更新用户
        user_dict = data.model_dump(exclude_unset=True, exclude={"role_ids", "position_ids"})
        new_user = await UserCRUD(auth).update(id=data.id, data=user_dict)

        # 更新角色和岗位
        if data.role_ids and len(data.role_ids) > 0:
            # 检查角色是否都存在且可用
            roles = await RoleCRUD(auth).get_role_list(search={"id": ("in", data.role_ids)})
            if len(roles) != len(data.role_ids):
                raise CustomException(msg='部分角色不存在')
            if not all(role.available for role in roles):
                raise CustomException(msg='部分角色已被禁用')
            await UserCRUD(auth).set_user_roles(user_ids=[data.id], role_ids=data.role_ids)

        if data.position_ids and len(data.position_ids) > 0:
            # 检查岗位是否都存在且可用
            positions = await PositionCRUD(auth).get_position_list(search={"id": ("in", data.position_ids)})
            if len(positions) != len(data.position_ids):
                raise CustomException(msg='部分岗位不存在')
            if not all(position.available for position in positions):
                raise CustomException(msg='部分岗位已被禁用')
            await UserCRUD(auth).set_user_positions(user_ids=[data.id], position_ids=data.position_ids)

        user_dict = UserOutSchema.model_validate(new_user).model_dump()
        return user_dict

    @classmethod
    async def delete_user(cls, auth: AuthSchema, id: int) -> None:
        """删除用户"""
        user = await UserCRUD(auth).get_user_by_id(id=id)
        if not user:
            raise CustomException(msg="用户不存在")
        if user.is_superuser:
            raise CustomException(msg="超级管理员不能删除")
        if user.available:
            raise CustomException(msg="用户已启用,不能删除")
        if auth.user.id == id:
            raise CustomException(msg="不能删除当前登陆用户")
        # 删除用户角色关联数据
        await UserCRUD(auth).set_user_roles(user_ids=[id], role_ids=[])
        
        # 删除用户岗位关联数据
        await UserCRUD(auth).set_user_positions(user_ids=[id], position_ids=[])
        
        # 删除用户
        await UserCRUD(auth).delete(ids=[id])

    @classmethod
    async def get_current_user_info(cls, auth: AuthSchema) -> Dict:
        """获取当前用户信息"""
        # 获取用户基本信息
        user = await UserCRUD(auth).get_user_by_id(id=auth.user.id)
        if not user:
            raise CustomException(msg="用户不存在")
        dept = await DeptCRUD(auth).get_dept_by_id(id=user.dept_id)
        user.dept_name = dept.name if dept else None
        user_dict = UserOutSchema.model_validate(user).model_dump()

        # 获取菜单权限
        if auth.user.is_superuser:
            menu_all = await MenuCRUD(auth).get_menu_list(search={'type': ('in', [1, 2]), 'available': True})
            menus = [MenuOutSchema.model_validate(menu).model_dump() for menu in menu_all]
        else:
            menus = [
                MenuOutSchema.model_validate(menu).model_dump()
                for role in auth.user.roles
                for menu in role.menus
                if menu.available and menu.type in [1, 2]
            ]
        user_dict["menus"] = menus
        return user_dict

    @classmethod
    async def update_current_user_info(cls, auth: AuthSchema, data: CurrentUserUpdateSchema) -> Dict:
        """更新当前用户信息"""
        user = await UserCRUD(auth).get_user_by_id(id=auth.user.id)
        if not user:
            raise CustomException(msg="用户不存在")
        new_user = await UserCRUD(auth).update(id=auth.user.id, data=data)
        return UserOutSchema.model_validate(new_user).model_dump()

    @classmethod
    async def set_user_available(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """设置用户状态"""
        for id in data.ids:
            user = await UserCRUD(auth).get_user_by_id(id=id)
            if not user:
                raise CustomException(msg=f"用户ID {id} 不存在")
            if user.is_superuser:
                raise CustomException(msg="超级管理员状态不能修改")
        await UserCRUD(auth).set_user_available(ids=data.ids, available=data.available)

    @classmethod
    async def upload_avatar(cls, request: Request, file: UploadFile) -> Dict:
        """上传头像"""
        if not file:
            raise CustomException(msg="请选择要上传的文件")
        filename, filepath = await UploadUtil.upload_file(file=file)
        
        return UploadResponseSchema(
            file_path=f'{filepath}',
            file_name=filename,
            origin_name=file.filename,
            file_url=f'{request.base_url}{filepath}',
        ).model_dump()

    @classmethod
    async def change_user_password(cls, auth: AuthSchema, data: UserChangePasswordSchema) -> Dict:
        """修改用户密码"""
        if not data.old_password or not data.new_password:
            raise CustomException(msg='密码不能为空')

        # 验证原密码
        user = await UserCRUD(auth).get_user_by_id(id=auth.user.id)
        if not user:
            raise CustomException(msg="用户不存在")
        if not PwdUtil.verify_password(plain_password=data.old_password, password_hash=user.password):
            raise CustomException(msg='原密码输入错误')

        # 更新密码
        new_password_hash = PwdUtil.set_password_hash(password=data.new_password)
        new_user = await UserCRUD(auth).change_password(id=user.id, password_hash=new_password_hash)
        return UserOutSchema.model_validate(new_user).model_dump()

    @classmethod
    async def register_user(cls, auth: AuthSchema, data: UserRegisterSchema) -> Dict:
        """用户注册"""
        # 检查用户名是否存在
        user = await UserCRUD(auth).get_user_by_username(username=data.username)
        if user:
            raise CustomException(msg='用户名已存在')

        data.password = PwdUtil.set_password_hash(password=data.password)
        dict_data = data.model_dump(exclude_unset=True)
        dict_data['creator_id'] = data.creator_id
        dict_data['dept_id'] = data.dept_id
        dict_data['description'] = data.description
        result = await UserCRUD(auth).create(data=dict_data)
        await UserCRUD(auth).set_user_roles(user_ids=[result.id], role_ids=data.role_ids)
        await UserCRUD(auth).set_user_positions(user_ids=[result.id], position_ids=data.position_ids)
        return UserOutSchema.model_validate(result).model_dump()

    @classmethod
    async def forget_password(cls, auth: AuthSchema, data: UserForgetPasswordSchema) -> Dict:
        """用户忘记密码"""
        user = await UserCRUD(auth).get_user_by_username(username=data.username)
        if not user:
            raise CustomException(msg="用户不存在")
        if not user.available:
            raise CustomException(msg="用户已停用")
        if user.mobile != data.mobile:
            raise CustomException(msg="手机号不匹配")
        new_password_hash = PwdUtil.set_password_hash(password=data.new_password)
        new_user = await UserCRUD(auth).forget_password(id=user.id, password_hash=new_password_hash)
        return UserOutSchema.model_validate(new_user).model_dump()

    @classmethod
    async def batch_import_user(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> Dict:
        """批量导入用户"""

        header_dict = {
            '部门编号': 'dept_id',
            '用户名': 'username',
            '名称': 'name',
            '邮箱': 'email',
            '手机号': 'mobile',
            '性别': 'gender',
            '状态': 'available'
        }

        try:
            # 读取Excel文件
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            await file.close()
            
            # 重命名列名
            df.rename(columns=header_dict, inplace=True)
            
            # 验证必填字段
            required_fields = ['username', 'name', 'dept_id']
            for field in required_fields:
                if df[field].isnull().any():
                    raise CustomException(msg=f"{header_dict[field]}不能为空")
            
            error_msgs = []
            success_count = 0
            
            # 处理每一行数据
            for index, row in df.iterrows():
                try:
                    # 数据转换
                    row['gender'] = 1 if row['gender'] == '男' else (2 if row['gender'] == '女' else 1)
                    row['available'] = True if row['available'] == '正常' else False
                    
                    # 检查部门是否存在
                    dept = await DeptCRUD(auth).get_dept_by_id(id=int(row['dept_id']))
                    if not dept:
                        raise CustomException(msg=f"部门ID {row['dept_id']} 不存在")
                    
                    # 构建用户数据
                    user_data = UserCreateSchema(
                        username=str(row['username']).strip(),
                        name=str(row['name']).strip(),
                        email=str(row['email']).strip() if not pd.isna(row['email']) else None,
                        mobile=str(row['mobile']).strip() if not pd.isna(row['mobile']) else None,
                        gender=row['gender'],
                        available=row['available'],
                        dept_id=int(row['dept_id']),
                        password="123456" # 设置默认密码
                    )

                    # 处理用户导入
                    exists_user = await UserCRUD(auth).get_user_by_username(username=user_data.username)
                    if exists_user:
                        if update_support:
                            await UserCRUD(auth).update(id=exists_user.id, data=user_data)
                            success_count += 1
                        else:
                            error_msgs.append(f"第{index+1}行: 用户 {user_data.username} 已存在")
                    else:
                        await UserCRUD(auth).create(data=user_data)
                        success_count += 1
                        
                except Exception as e:
                    error_msgs.append(f"第{index+1}行: {str(e)}")
                    continue

            return {
                "success": True,
                "message": f"成功导入 {success_count} 条数据" + ("\n" + "\n".join(error_msgs) if error_msgs else "")
            }
            
        except Exception as e:
            raise CustomException(msg=f"导入失败: {str(e)}")

    @classmethod
    async def get_import_template_user(cls) -> bytes:
        """获取用户导入模板"""
        header_list = ['部门编号', '用户名', '名称', '邮箱', '手机号', '性别', '状态']
        selector_header_list = ['性别', '状态'] 
        option_list = [{'性别': ['男', '女', '未知']}, {'状态': ['正常', '停用']}]
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )

    @classmethod
    async def export_user_list(cls, user_list: List[Dict[str, Any]]) -> bytes:
        """导出用户列表"""
        if not user_list:
            raise CustomException(msg="没有数据可导出")
            
        # 定义字段映射
        mapping_dict = {
            'id': '用户编号',
            'username': '用户名称',
            'name': '用户昵称', 
            'dept_name': '部门',
            'email': '邮箱地址',
            'mobile': '手机号码',
            'gender': '性别',
            'available': '状态',
            'creator': '创建者',
            'create_datetime': '创建时间',
            'modifier': '更新者', 
            'update_datetime': '更新时间',
            'description': '备注'
        }

        # 复制数据并转换
        data = user_list.copy()
        for item in data:
            item['available'] = '正常' if item.get('available') else '停用'
            gender = item.get('gender')
            item['gender'] = '男' if gender == 1 else ('女' if gender == 2 else '未知')

        # 转换为中文键
        new_data = [
            {mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} 
            for item in data
        ]

        return ExcelUtil.export_list2excel(list_data=new_data)
