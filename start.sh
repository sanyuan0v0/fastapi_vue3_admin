cd /home
rm -rf fastapi_vue3_admin/
git clone https://gitee.com/tao__tao/fastapi_vue3_admin.git
cd fastapi_vue3_admin/frontend
npm install
npm run build
cd  home/fastapi_vue3_admin
docker compose kill
docker compose build
docker compose up -d  --force-recreate 

