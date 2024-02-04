# Vue-Multiselect下拉框强化插件的使用

- 插件主页： [https://www.vue-multiselect.cn/](https://www.vue-multiselect.cn/)
- 入门和示例： [https://www.vue-multiselect.cn/#sub-getting-started](https://www.vue-multiselect.cn/#sub-getting-started)

具体可参考官方示例。

此处直接上代码，各选项的说明都在代码中：

```html
<!DOCTYPE html>
<!-- testselect.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>Vue-Multiselect下拉框强化插件的使用</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
		<script src="https://unpkg.com/vue-multiselect@2.1.0"></script>
		<link rel="stylesheet" href="https://unpkg.com/vue-multiselect@2.1.0/dist/vue-multiselect.min.css">
	</head>
	<body>

		<div id="app">
			<div>
				<!-- 各参数意义解释
				 multiselect需要与`Vue.component('multiselect'`行定义的组件名称相同
				 v-model="value" 值绑定到value数据中
				 :options="options" 可用选项的数组
				 :multiple="true" 支持多选
				 :close-on-select="true" 选择选项后，下拉菜单设置为关闭状态，这样减少页面显示区域
				 :clear-on-select="false" 选择一个选项后，搜索查询保持不变
				 :hide-selected="true" 已经选择的选项将不会显示在下拉菜单中
				 :options-limit="20" 将显示的选项限制为20个，避免显示太多
				 :preserve-search="true" 在打开/关闭组件时将保留搜索查询。
				 placeholder="选择用户" 下拉框的占位符
				 label="name" 和  track-by="name" 使用对象时，必须提供其他道具：label 和 track-by.
					track-by用于标识选项列表中的选项，因此其值必须唯一。在此示例中，该name属性在所有选项中都是唯一的，因此可以将其用作track-by值。
					label用于显示选项。
				 select-label="单击或按回车选择" 对应selectLabel，指向选项时显示的字符串 
				 :showNoResults="true" 如果未找到结果，则显示noResult插槽，插槽由`<span slot="noResult">未搜索到该用户,请更改搜索查询</span>`进行定义
				 :custom-label="customLabel" 用于自定义选项的显示样式，custom-label接受一个以option 对象为第一个参数的函数。它应该返回一个字符串，然后将其用于显示自定义标签。
				 -->
				<multiselect v-model="value" :options="options" :multiple="true" :close-on-select="true"
					:clear-on-select="false" :hide-selected="true" :options-limit="20" :preserve-search="true"
					placeholder="选择用户" label="name" track-by="name" select-label="单击或按回车选择" :showNoResults="true"
					:custom-label="customLabel">
					<span slot="noResult">未搜索到该用户,请更改搜索查询</span>
				</multiselect>
			</div>
			<pre class="language-json"><code>{{ value }}</code></pre>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			Vue.component('multiselect', window.VueMultiselect.default)
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					value: null,
					options: [{
							name: 'Vue.js',
							language: 'JavaScript'
						},
						{
							name: 'Rails',
							language: 'Ruby'
						},
						{
							name: 'Sinatra',
							language: 'Ruby'
						},
						{
							name: 'Laravel',
							language: 'PHP'
						},
						{
							name: 'Phoenix',
							language: 'Elixir'
						}
					]
				},
				methods: {
					other: function() {
						console.log('common function.')
					},
					customLabel: function({
						name,
						language
					}) {
						return `${name} – ${language}`
					}
				}
			})
		</script>
	</body>
</html>

```

运行后，打开URL。

效果图：

初始状态：

![](/img/20210519220652.png)

选择选项后：

![](/img/20210519220737.png)

搜索时：

![](/img/20210519220833.png)

所有选项都选中后：

![](/img/20210519220919.png)



