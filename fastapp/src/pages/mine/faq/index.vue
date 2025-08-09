<template>
  <view class="faq-container">
    <view class="wechat">
      <view class="tips">
        <text>长按关注「有来技术」公众号，获取交流群二维码。</text>
      </view>
      <view class="flex-center">
        <image
          class="w-158px h-158px"
          :show-menu-by-longpress="true"
          src="/static/images/qrcode-official.png"
          mode="aspectFit"
        />
      </view>
      <view>
        <text>如果交流群的二维码过期，请加微信(</text>
        <text :user-select="true" :selectable="true">haoxianrui</text>
        <text>)并备注「前端」、「后端」或「全栈」以获取最新二维码。</text>
      </view>
      <view>
        <text>为确保交流群质量，防止营销广告人群混入，我们采取了此措施。望各位理解！</text>
      </view>
    </view>

    <wd-collapse v-model="value">
      <wd-collapse-item title="开源项目issues" name="item1">
        <!-- #ifdef H5 -->
        <a href="https://gitee.com/youlaiorg/vue-uniapp-template/issues">#issues</a>
        <!-- #endif -->
        <!-- #ifdef MP-WEIXIN -->
        <text :user-select="true">https://gitee.com/youlaiorg/vue-uniapp-template/issues</text>
        <!-- #endif -->
      </wd-collapse-item>
      <wd-collapse-item title="小程序分包" name="item2">
        <view>
          <text>
            分包主要是因为小程序平台对主包大小有限制（微信小程序的规则是主包不超过2M，每个分包不超过2M，总体积一共不能超过20M），
            分包不需要按照业务模块来分，可以将多个业务模块放入一个分包中，直到这个分包达到小程序的大小限制才考虑下一个分包。
            uniapp的用法与微信官方文档一样，具体参见：
          </text>
          <!-- #ifdef H5 -->
          <a
            href="https://developers.weixin.qq.com/miniprogram/dev/framework/subpackages/basic.html"
          >
            微信官方文档-分包
          </a>
          <!-- #endif -->
          <!-- #ifdef MP-WEIXIN -->
          <text :user-select="true" :selectable="true">
            https://developers.weixin.qq.com/miniprogram/dev/framework/subpackages/basic.html
          </text>
          <!-- #endif -->
        </view>
        <view class="mt-15rpx">
          <text>
            以下是一个简单示例。以下示例中创建了两个分包，分包a中包含两个页面，分包b中包含一个页面。
          </text>
          <text class="mt-15rpx">
            请注意，如果想把分包页面中使用的组件打包到分包中，则需要将组件放入对应的分包目录下，否则组件会被打包到主包中。
          </text>
        </view>
        <view class="mt-15rpx">
          <text>目录结构：</text>
        </view>
        <rich-text :nodes="subListStr" />
        <view class="mt-15rpx">
          <text>在pages.json文件中声明分包结构：</text>
        </view>
        <rich-text :nodes="pagesStr" />
      </wd-collapse-item>
    </wd-collapse>
  </view>
</template>

<script lang="ts" setup>
const value = ref<string[]>(["item1"]);
const subListStr = ref<string>(`
<pre style="background-color: #f9f9fa"><code>
|-- components    //主包组件目录
|-- pages         //主包页面目录
|   |-- index
|-- sub-pkg-a
|   |-- components    //分包组件目录
|   |-- pages         //分包页面目录
|   |   |-- cat
|   |   |-- dog
|-- sub-pkg-b
|   |-- components    //分包组件目录
|   |-- pages         //分包页面目录
|   |   |-- apple</code></pre>
`);

const pagesStr = ref<string>(`<pre style="background-color: #f9f9fa"><code>
{
  "pages":[
    {
      "path": "pages/index",
      "style": {
        "navigationBarTitleText": "主页"
      }
    }
  ],
  "subPackages": [
    {
      "root": "sub-pkg-a",
      "pages": [
        {
          "path": "pages/cat",
          "style": {
            "navigationBarTitleText": "cat"
          }
        },
        {
          "path": "pages/dog",
          "style": {
            "navigationBarTitleText": "dog"
          }
        }
      ]
    },
    {
      "root": "sub-pkg-b",
      "pages": [
        {
          "path": "pages/apple",
          "style": {
            "navigationBarTitleText": "apple"
          }
        }
      ]
    }
  ]
}</code></pre>
`);
onMounted(() => {});
</script>

<style lang="scss" scoped>
.faq-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  .wechat {
    padding: 30rpx;
    margin: 20px 0;
    font-size: 14px;
    color: var(--wot-card-content-color, rgba(0, 0, 0, 0.45));
    background-color: #fff;
    .tips {
      font-weight: bold;
      text-align: center;
    }
  }
}
</style>
