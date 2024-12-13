# Markdown转静态网站（mkdocs-material使用）

## 工具介绍

- 名称：mkdocs-material
- 官网：<https://squidfunk.github.io/mkdocs-material/>
- 完整文档信息清访问 [mkdocs官网](https://www.mkdocs.org).

## 工具安装

```sh
pip install mkdocs-material
```

## 工具使用

### 创建项目

```sh
mkdocs new 项目名称
```

### 编辑构建文档

```yaml
theme:
  name: material
```

### 启动服务

```sh
mkdocs serve
```

### 构建静态站点

```sh
mkdocs build
```

### 获取帮助

```sh
mkdocs -h
```

### 生成所有依赖

```sh
pip freeze > requirements.txt
```

