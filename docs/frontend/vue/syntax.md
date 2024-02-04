# 模板语法

[[toc]]

Vue.js 使用了基于 HTML 的模板语法，允许开发者声明式地将 DOM 绑定至底层 Vue 实例的数据。所有 Vue.js 的模板都是合法的 HTML，所以能被遵循规范的浏览器和 HTML 解析器解析。

在底层的实现上，Vue 将模板编译成虚拟 DOM 渲染函数。结合响应系统，Vue 能够智能地计算出最少需要重新渲染多少组件，并把 DOM 操作次数减到最少。

如果你熟悉虚拟 DOM 并且偏爱 JavaScript 的原始力量，你也可以不用模板，[直接写渲染 (render) 函数](https://cn.vuejs.org/v2/guide/render-function.html)，使用可选的 JSX 语法。

## 1. 插值

### 1.1 文本

使用Mustache语法(双大括号)的文本插值是最常见的数据绑定形式。数据对象发生变化时，插值处的内容一般会发生变更。

Mustache英文的意思是`胡子`，`{{}}`就像人的胡子。

但应注意的是，如果使用`v-once`指令进行插值时，当数据发生变更时，插值处的内容不会更新。

请看如下示例。

```html
<!DOCTYPE html>
<!-- filename:text_mustache.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<span>Message: {{ message }}</span><br>
			<span v-once>Msg: {{ msg }}</span><br>
			<button v-on:click="changeMessage">Change Message</button>
			<button v-on:click="changeOnceMessage">Change Once Message</button>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			// 在引用vue.js时，会声明一个全局变量Vue
			// 通过`new Vue`的方式可以获取一个Vue的应用
			// 它会返回一个对象，我们称之为应用对象，如`app`
			// 在`new Vue`时需要注意的时候，需要传入一个对象{}作为参数
			// 这个对象{}有两个非常重要的属性，el和data
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					message: "消息",
					msg: "不能变的消息",
				},
				methods:{
					changeMessage: function() {
						this.message = 'new message'
					},
					changeOnceMessage: function() {
						this.msg = 'new msg'
					}
				}
			})
		</script>
	</body>
</html>

```

打开浏览器查看，初始状态下信息显示如下：

![](/img/20210512222139.png)

分别点击`Change Message`和`Change Once Message`，此时，可以看到`vue-devtools`中的`message`和`msg`都发生了变化，但界面上只有`Message`行发生了变化，变成了`new message`，而`Msg`行并没有发生变化。

![](/img/20210512222457.png)

说明，使用`v-once`只会进行一次插值，数据更新后，页面内容不会发生变化。

### 1.2 原始html

如果双大括号中的原始数据是html类型的数据，Vue会将其字符直接原样输出。如果要将其转换成真正的HTML，则需要使用`v-html`指令。请看如下示例：

```html
<!DOCTYPE html>
<!-- filename:rawHtml.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>解析HTML代码</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<p>Using mustaches: {{ rawHtml }}</p>
			<p>Using v-html directive: <span v-html="rawHtml"></span></p>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					rawHtml: '<span style="color: red;">This should be red.</span>',
				}
			})
		</script>
	</body>
</html>

```

运行后，在浏览器中查看的效果如下：

![](/img/20210512232500.png)

可以看到使用双大括号解析的数据当作字符串原样输出。而通过`v-html`指令将`rawHtml`数据解析成html标签数据,成功显示了红色样式字体。



::: danger 危险
你的站点上动态渲染的任意 HTML 可能会非常危险，因为它很容易导致 [XSS 攻击](https://en.wikipedia.org/wiki/Cross-site_scripting)。请只对可信内容使用 HTML 插值，**绝不要**对用户提供的内容使用插值。
:::

注意，你不能使用 v-html 来复合局部模板，因为 Vue 不是基于字符串的模板引擎。反之，对于用户界面 (UI)，组件更适合作为可重用和可组合的基本单位。

### 1.3 Attribute属性

Mustache双大括号语法不能应用于HTML Attribute属性上，此时应使用`v-bind`指令。对于布尔属性(只要存在则意味着`true`)，`v-bind`工作起来有所不同。请看以下示例。

![](/img/20210513081155.png)

可以看到，在属性中直接使用

```html 
id="{{ dynamicId }}"`
```

并没有正常解析出id值，而通过`v-bind:id="dynamicId"`则正常解析出id值了。

`<button disabled>`中`disabled`中不带任何值时，按钮也是不可用的，说明只要存在`disabled`属性则其值就是`true`。

`<button v-bind:disabled="isButtonDisabled">`中通过解析`isButtonDisabled`属性的值来确定按钮是否可用。如果我们将`isButtonDisabled`设置为`false`，则按钮可点击。



我们可以通过事件（如点击事件）来改变按钮的`disabled`属性。

```html
<!DOCTYPE html>
<!-- html_attribute.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>双大括号应用于HTML属性</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<p id="{{ dynamicId }}">mustache id</p>
			<p v-bind:id="dynamicId">v-bind id</p>
			<button disabled>Use default disabled Button</button>
			<button v-bind:disabled="isButtonDisabled">Use v-bind:disabled Button</button>
			<button v-on:click="changeDisable">Change</button>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					dynamicId: 'dynamic_id',
					isButtonDisabled: true,
				},
				methods:{
					changeDisable () {
						console.log('change disable attribute')
						this.isButtonDisabled = !this.isButtonDisabled
					}
				}
			})
		</script>
	</body>
</html>

```

此时点击`Change`按钮可以切换左边`Use v-bind:disabled Button`按钮的显示状态。可以在禁用和非禁用状态来回切换。



### 1.4 使用JavaScript表达式

- 对于所有的数据绑定，Vue.js 都提供了完全的 JavaScript 表达式支持。
- 每个绑定都只能包含**单个表达式**。

按官方示例。我们编写`use_js.html`文件：

```html
<!DOCTYPE html>
<!-- use_js.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>模板中使用JavaScript表达式</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<!-- 正式解析的表达式 -->
			{{ number + 1 }}
			{{ ok ? 'YES' : 'NO' }}
			{{ message.split('').reverse().join('') }}
			<div v-bind:id="'list-' + id"></div>
			
			<!-- 这是语句，不是表达式 -->
			<!-- {{ var a = 1 }} -->
			<!-- 流控制也不会生效，请使用三元表达式 -->
			<!-- {{ if (ok) { return message } }} -->
			<!-- 尝试访问用户自定义的全局变量，不能访问 -->
			<!-- {{ LANG }} -->
			<!-- 使用内置全局变量 -->
			Date()={{ Date() }}<br>
			Boolean()={{ Boolean() }}<br>
			Boolean(0)={{ Boolean(0) }}<br>
			Boolean(1)={{ Boolean(1) }}<br>
			Boolean(-1)={{ Boolean(-1) }}<br>
			Math.PI={{ Math.PI }}<br>
			Number('0.123')={{ Number('0.123') }}<br>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			const LANG = 'VUE' // 增加此行
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					number: 1,
					ok: true,
					message: 'Hello,Vue.js!',
					id: 2,
				},		
			})
		</script>
	</body>
</html>

```



此时页面正常解析，页面显示如下：

![img](/img/20210516103240.png)

此时`div`的id值也能正常解析：

![img](/img/20210516103430.png)

我们如果把19行的取消注释，此时页面解析会报错：

![img](/img/20210516103654.png)

提示`avoid using JavaScript keyword as property name: "var"`禁止使用关键字`var`作为属性名。同样，如果将21行取消注释。也会报异常`avoid using JavaScript keyword as property name: "if"`禁止使用关键字`if`作为属性名。

官方文档中指出：

::: warning 警告

模板表达式都被放在沙盒中，只能访问[全局变量的一个白名单](https://github.com/vuejs/vue/blob/v2.6.10/src/core/instance/proxy.js#L9)，如 `Math` 和 `Date` 。你不应该在模板表达式中试图访问用户定义的全局变量。

:::

- 沙盒（英语：sandbox，又译为沙箱）：计算机术语，在计算机安全领域中是一种安全机制，为运行中的程序提供的隔离环境。沙盒通常严格控制其中的程序所能访问的资源。

- Vue将模板表达式放在封闭环境中，定义其只能访问指定的全局变量（白名单），所以自定义的全局变量无法在模板表达式中使用。

如我们在Javascript中定义一个全局变量`const LANG = 'VUE'`:

```javascript
		<script>
			const LANG = 'VUE' // 增加此行
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				...省略
```

然后在上面增加内容：

```html
			<!-- 尝试访问用户自定义的全局变量 -->
			{{ LANG }}
```



此时提示异常`vue.js:634 [Vue warn]: Property or method "LANG" is not defined on the instance but referenced during render.`：

![img](/img/20210516110508.png)

实例中属性或方法`LANG`没有定义。说明这种方式使用全局变量是错误的。

[https://github.com/vuejs/vue/blob/v2.6.10/src/core/instance/proxy.js#L9](https://github.com/vuejs/vue/blob/v2.6.10/src/core/instance/proxy.js#L9)  中定义了一些全局变量：

```javascript
if (process.env.NODE_ENV !== 'production') {
  const allowedGlobals = makeMap(
    'Infinity,undefined,NaN,isFinite,isNaN,' +
    'parseFloat,parseInt,decodeURI,decodeURIComponent,encodeURI,encodeURIComponent,' +
    'Math,Number,Date,Array,Object,Boolean,String,RegExp,Map,Set,JSON,Intl,' +
    'require' // for Webpack/Browserify
  )
```

我们可以尝试使用其中的一些变量：

```html
			Date()={{ Date() }}<br>
			Boolean()={{ Boolean() }}<br>
			Boolean(0)={{ Boolean(0) }}<br>
			Boolean(1)={{ Boolean(1) }}<br>
			Boolean(-1)={{ Boolean(-1) }}<br>
			Math.PI={{ Math.PI }}<br>
			Number('0.123')={{ Number('0.123') }}<br>
```

最后在页面上显示如下：

![](/img/20210516121618.png)

其他的一些变量后面实际中遇到后再使用。



## 2. 指令与缩写

指令 (Directives) 是带有 `v-` 前缀的特殊特性。指令特性的值预期是**单个 JavaScript 表达式** (`v-for` 是例外情况，稍后我们再讨论)。指令的职责是，当表达式的值改变时，将其产生的连带影响，响应式地作用于 DOM。

我们在 [指令](./vue_basic_use.html#_2-指令) 中已经使用过`v-bind`、`v-if`、`v-for`、`v-on`、`v-model`等指令。

- `v-if`指令

```html
<p v-if="seen">现在你看到我了</p>
```

当`seen`属性的值为`true`时，页面会上渲染`p`标签的内容。当值为`false`时，页面上不会渲染`p`标签的内容。

### 2.1 参数

一些指令能够接收一个“参数”，在指令名称之后以冒号表示。

- `v-bind`指令

我们在 [v-bind属性绑定指令](vue_basic_use.html#_2-1-v-bind属性绑定指令) 中已经使用过`v-bind:title`来绑定一个`title`属性。

此处官方示例：

```html
<a v-bind:href="url">...</a>
```

当点击`...`则会打开对应的URL地址，如果在Vue对象的`data`属性中定义`url:'https://cn.vuejs.org/v2/guide/'`，则点击`...`时会打开Vue的官方教程。

这里`href`是`v-bind`的参数，告知`v-bind`将该元素的`href`属性与表达式的`url`的值绑定。

- `v-on`指令

我们在 [v-on事件监听指令](vue_basic_use.html#_2-4-v-on事件监听指令)中已经使用`v-on:click`指令来监听点击事件。

此处我们使用`<input type="text" v-on:blur="echo">`来监听输入框失去焦点事件，当鼠标从输入框中移出时，自动触发`echo`函数的执行，输出警告并打印日志信息：

![](/img/20210516173214.png)

后面有章节会详细介绍事件处理。

### 2.2 动态参数

从 2.6.0 开始，可以用方括号括起来的 JavaScript 表达式作为一个指令的参数。

如我们在HTML中增加以下代码，尝试使用动态参数：

```html
<!-- 动态参数 -->
<a v-bind:[attributeName]="url">...</a>
```

然后在`data`属性中定义`attributeName: 'href'`,此时打开页面，会发现抛出异常。

![](/img/20210516181203.png)

可以看到属性`attributeName`会强制转换成了小写`attributename`。官方文档中也指出：

::: warning 警告

在 DOM 中使用模板时 (直接在一个 HTML 文件里撰写模板)，还需要避免使用大写字符来命名键名，因为浏览器会把 attribute 名全部强制转为小写。

:::

我们将html和data中`attributeName`转换成小写`attributename`，然后再打开页面。此时没有报异常，并且正常渲染了`href`属性。

![](/img/20210516181712.png)

我们在控制台修改一下attributename的值：

![](/img/20210516181837.png)

此时，可以看到`href`属性已经没有了，出现了`title`属性：

![](/img/20210516181949.png)



使用动态参数绑定事件名。

可以在 [HTML 事件属性](https://www.runoob.com/tags/ref-eventattributes.html) 获取HTML中有哪些事件属性。

我们尝试使用以下几个属性：

- `onfocus` 当窗口获得焦点时运行脚本
- `onblur` 当窗口失去焦点时运行脚本
- `onmouseover` 当鼠标指针移至元素之上时运行脚本
- `onmousemove` 当鼠标指针移动时运行脚本

在html中增加以下代码：

```html
<a v-on:[eventname]="doSomething" v-bind:href="url">事件属性</a>
...省略
				data: {
					...省略
					eventname: 'focus'
				},
				methods: {
					...省略
					doSomething: function() {
						if (this.eventname === 'focus') {
							console.log('获得焦点');
						} else if (this.eventname === 'blur') {
							console.log('失去焦点');
						} else if (this.eventname === 'mouseover') {
							console.log('鼠标指针移至元素之上');
						} else if (this.eventname === 'mouseout') {
							console.log('鼠标指针移出元素');
						}
					}
				}
```

`eventname`初始值设置为`foucus`。我们打开页面，按`Tab`键，当切换到`事件属性`时，可以看到控制台输出`获得焦点`。

然后在控制台设置一下`app.eventname = 'blur'`，此时鼠标点击一下页面中间的空白，控制台会输出`失去焦点`。

然后在控制台设置一下`app.eventname = 'mouseover'`，此时将鼠标移动到`事件属性`字符处，控制台会输出`鼠标指针移至元素之上`。

然后在控制台设置一下`app.eventname = 'mouseout'`，此时先将鼠标移动到`事件属性`字符处然后移开，控制台会输出`鼠标指针移出元素`。

![](/img/20210516194151.png)

本节使用的代码如下：

```html
<!DOCTYPE html>
<!-- directives.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>指令的使用</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<p v-if="seen">现在你看到我了</p>
			<a v-bind:href="url">...</a><br>
			<!-- 当窗口失去焦点时运行脚本 -->
			<input type="text" v-on:blur="echo"><br>
			<!-- 动态参数 -->
			<!-- 避免使用大写字符来命名键名，因为浏览器会把 attribute 名全部强制转为小写 -->
			<!-- <a v-bind:[attributeName]="url">...</a> -->
			<!-- 属性使用小写时，才能正常解析 -->
			<a v-bind:[attributename]="url">...</a>
			<!-- 同样，在单独的HTML文件中，不能直接使用大写的eventName变量 -->
			<!-- 下面语句会提示eventname属性不存在 -->
			<!-- <a v-on:[eventName]="doSomething"> ... </a> -->
			<a v-on:[eventname]="doSomething" v-bind:href="url">事件属性</a>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					seen: true,
					url: 'https://cn.vuejs.org/v2/guide/',
					attributename: 'href',
					eventname: 'focus'
				},
				methods: {
					echo: function() {
						console.log('you left me.')
						alert('you left me.')
					},
					doSomething: function() {
						if (this.eventname === 'focus') {
							console.log('获得焦点');
						} else if (this.eventname === 'blur') {
							console.log('失去焦点');
						} else if (this.eventname === 'mouseover') {
							console.log('鼠标指针移至元素之上');
						} else if (this.eventname === 'mouseout') {
							console.log('鼠标指针移出元素');
						}
					}
				}
			})
		</script>
	</body>
</html>

```

另外，动态表达式有一些语法约束。如不能包含空格和引号。



### 2.3 修饰符

修饰符 (modifier) 是以半角句号 `.` 指明的特殊后缀，用于指出一个指令应该以特殊方式绑定。

在 [事件处理](https://cn.vuejs.org/v2/guide/events.html) 章节详细介绍了修饰符的使用。

如`事件修饰符`、`按键修饰符`、`系统修饰键`等。

我们来看一下不使用修饰符时，对div进行点击时，会出现什么效果。

```html
<!DOCTYPE html>
<!-- modifiers.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>修饰符(modifier)的使用</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
		<style>
			.div1 {
				width: 100px;
				height: 50px;
				border-style:solid;
				border-color: red;
				background: green;
				margin-left: 50px;
			}
			.div2 {
				width: 50px;
				height: 100px;
				border-style:solid;
				border-color: blue;
				background: skyblue;
				margin-left: 25px;
				margin-top: 25px;
			}
		</style>
	</head>
	<body>
		<div id="app">
			<!-- 修饰符 (modifier) 是以半角句号 . 指明的特殊后缀 -->
			<div id="div1" v-on:click="click1()" class="div1">
				<!-- 不使用修饰符 (modifier) -->
				<!-- <div id="div2" v-on:click="click2()" class="div2"> -->
				<!-- 修饰符 (modifier) 是以半角句号 . 指明的特殊后缀 -->
				<div id="div2" v-on:click.stop="click2()" class="div2">
					点击我
				</div>
			</div>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					test: true
				},
				methods: {
					click1: function() {
						console.log('you clicked the div1')
					},
					click2: function() {
						console.log('you clicked the div2')
					},
				}
			})
		</script>
	</body>
</html>

```

此时我们打开页面`http://127.0.0.1:8848/vuedata/modifiers.html`,看到如下图所示页面：

![](/img/20210516204519.png)



我们点击`div1`的绿色区域，此时控制台显示`you clicked the div1`。

我们点击`div2`的天蓝色区域，此时控制台显示`you clicked the div2`并显示了`you clicked the div1`。

因为`div2`与`div1`有部分区域重叠，所有点击`div2`时，相当于同时点击了`div1`，所以显示了两条语句。

![](/img/20210516210543.png)

而如果我们在`div2`的点击事件中增加一个`stop`修饰符，此时的现象则会不一样。

```html
<!-- <div id="div2" v-on:click="click2()" class="div2"> -->
<div id="div2" v-on:click.stop="click2()" class="div2">
```

注意`v-on:click.stop`中`.stop`是修饰符，用于阻止单击事件继续传播 。



此时，我们再进行上述操作：

我们点击`div1`的绿色区域，此时控制台显示`you clicked the div1`。

我们点击`div2`的天蓝色区域，此时控制台显示`you clicked the div2`。没有显示其他的信息。说明单击事件传播已经被成功阻止了。

![](/img/20210516210904.png)

说明修饰符已经起作用了。

后续在事件处理章节再详细了解其他修饰符的使用。



### 2.4 说说缩写

此处抄一下官方的说明和示例。

`v-` 前缀作为一种视觉提示，用来识别模板中 Vue 特定的属性。当你在使用 Vue.js 为现有标签添加动态行为 (dynamic behavior) 时，`v-` 前缀很有帮助，然而，对于一些频繁用到的指令来说，就会感到使用繁琐。同时，在构建由 Vue 管理所有模板的[单页面应用程序 (SPA - single page application)](https://en.wikipedia.org/wiki/Single-page_application) 时，`v-` 前缀也变得没那么重要了。因此，Vue 为 `v-bind` 和 `v-on` 这两个最常用的指令，提供了特定简写：

- `v-bind`缩写

```html
<!-- 完整语法 -->
<a v-bind:href="url">...</a>

<!-- 缩写 -->
<a :href="url">...</a>

<!-- 动态参数的缩写 (2.6.0+) -->
<a :[key]="url"> ... </a>
```

- `v-on`缩写

```html
<!-- 完整语法 -->
<a v-on:click="doSomething">...</a>

<!-- 缩写 -->
<a @click="doSomething">...</a>

<!-- 动态参数的缩写 (2.6.0+) -->
<a @[event]="doSomething"> ... </a>
```



虽然有时使用缩写形式很方便，但不提倡在程序中使用缩写。原因如下：

::: tip 提示

- 代码20%的时间在写，80%的时间在读，可读性比敲代码时的时间节省要重要得多，况且敲代码的时间，占整个工程的时间，其实并不多。

- 缩写，不是每个人都可以理解。对一部分而言很熟悉很明显的缩写，对另一部分人则不是。例如cli是什么？是command line interface的缩写，还是client的缩写？

- 缩写，不同的人，缩出来的结果不一样。甚至在同一个工程下，都可能出现不同的缩写，严重影响代码可读性和心情。



作者：Jiafu89

链接：https://www.jianshu.com/p/eff10b0c4970

来源：简书

著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

:::



因此，尽量还是写完整的语句。