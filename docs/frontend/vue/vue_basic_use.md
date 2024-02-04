# vue的基本使用

- vue官方文档：[https://cn.vuejs.org/v2/guide/](https://cn.vuejs.org/v2/guide/)
- vue官方指定的视频教程： [https://learning.dcloud.io/#/?vid=0](https://learning.dcloud.io/#/?vid=0)
- vue教程：[https://www.lookroot.cn/course/vuebasics/](https://www.lookroot.cn/course/vuebasics/)
- 可以安装Vue DevTools，参考 [Mac环境下安装Vue DevTools Vue.js的调试神器](https://www.jianshu.com/p/5cd1f9770ff7)
- Vue (读音 /vjuː/，类似于 **view**) 是一套用于构建用户界面的**渐进式框架**。与其它大型框架不同的是，Vue 被设计为可以自底向上逐层应用。
- 开始尝试vue时，可以简单的创建一个`html`文件，并引用cdn上面的`vue.js`文件。
- 官方视频教程中老师是使用的`HBuilder X`来进行编码的。我们也使用`HBuilder X`工具来学习vue。在官方下载 [https://www.dcloud.io/hbuilderx.html](https://www.dcloud.io/hbuilderx.html) 安装即可。

## 1. 第一个vue程序

参考官方文档，需要新建一个`html`文件。并引入`vue.js`引用。

使用`HBuilder X`新建一个`app1.html`的文件，新建后`HBuilder X`会自动为我们添加一些内容：

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
	</head>
	<body>
	</body>
</html>
```

视频教程中告诉我们引入`vue.js`文件需要在`<head></head>`头部标签中引用。

我们引入标签:

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
	</body>
</html>
```

在`head`头部标签内部增加了`<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>`，这样就引入了`vue.js`文件了。



在以上的基础上，我们`采用简洁的模板语法来声明式地将数据渲染进 DOM 的系统`,在`body`标签中增加内容：

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
		  {{ message }}
		</div>
		
		<!-- script脚本包裹了一段js代码 -->
		<script>
			// 在引用vue.js时，会声明一个全局变量Vue
			// 通过`new Vue`的方式可以获取一个Vue的应用
			// 它会返回一个对象，我们称之为应用对象，如`app`
			// 在`new Vue`时需要注意的时候，需要传入一个对象{}作为参数
			// 这个对象{}有两个非常重要的属性，el和data
			var app = new Vue({
			 // el: element 指代元素属性
			 // data: 指代码数据属性，用于保存数据。在视图中声明了哪些变量，就需要在data里面注册，并且为变量进行初始化赋值
			  el: '#app',   // 利用元素选择器方式选中app div对象
			  data: {
			    message: 'Hello Vue!'
			  }
			})
		</script>
	</body>
</html>
```

刚开始看操作指南的时候，不知道`<div>`标签以及`js`内容放在哪里。可以观看视频教程。

我们在浏览器中打开`http://127.0.0.1:8848/vuedata/app1.html`,在页面上可以看到`Hello Vue!`的字符，说明我们的程序起作用了。

我们打开浏览器的`Console`窗口，在其中输入命令:

```sh
app.message
"Hello Vue!"
app.message = 'Hello World!'
"Hello World!"
app.message
"Hello World!"
```

可以看到当修改`app.message = 'Hello World!'`修改`message`的值时，页面上的显示自动发生变化，自动变成“Hello World!”了。



## 2. 指令

### 2.1 v-bind属性绑定指令

在`声明与渲染`文档中，使用了`v-bind`指令来与元素属性与`xxx`保持一致。

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<!-- 将span的title属性与message保持一致 -->
			<span v-bind:title="message">
				鼠标悬停几秒钟查看此处动态绑定的提示信息！
			</span>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			// 在引用vue.js时，会声明一个全局变量Vue
			// 通过`new Vue`的方式可以获取一个Vue的应用
			// 它会返回一个对象，我们称之为应用对象，如`app`
			// 在`new Vue`时需要注意的时候，需要传入一个对象{}作为参数
			// 这个对象{}有两个非常重要的属性，el和data
			var app = new Vue({
				// el: element 指代元素属性
				// data: 指代码数据属性，用于保存数据。在视图中声明了哪些变量，就需要在data里面注册，并且为变量进行初始化赋值
				el: '#app', // 利用元素选择器方式选中app div对象
				data: {
					message: '页面加载于 ' + new Date().toLocaleString()
				}
			})
		</script>
	</body>
</html>
```

我们在浏览器中打开`http://127.0.0.1:8848/vuedata/app1.html`,将鼠标停留在字符`鼠标悬停几秒钟查看此处动态绑定的提示信息！`处，可以看到`title`属性显示出来`页面加载于 2021/5/6下午11:24:17`。

并打开`Elements`，选择该处字符，也可以看到`<span title="页面加载于 2021/5/6下午11:24:17">鼠标悬停几秒钟查看此处动态绑定的提示信息！</span>`，说明的确将`message`数据渲染到`span`的`title`属性当中了：

![](/img/20210506232847.png)

### 2.2 v-if条件判断指令

我们可以使用`v-if`指令来判断是否显示某个元素。如下示例：

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<!-- 使用v-on:click事件监听指令绑定点击事件 -->
			<button v-on:click="change">点击我，下面的字符将会消失(再次点击，则会显示)</button>
			<!-- 使用v-if指令进行条件判断,当seen为true时，才显示 -->
			<p v-if="seen">现在你看到我了</p>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			// 在引用vue.js时，会声明一个全局变量Vue
			// 通过`new Vue`的方式可以获取一个Vue的应用
			// 它会返回一个对象，我们称之为应用对象，如`app`
			// 在`new Vue`时需要注意的时候，需要传入一个对象{}作为参数
			// 这个对象{}有两个非常重要的属性，el和data
			var app = new Vue({
				// el: element 指代元素属性
				// data: 指代码数据属性，用于保存数据。在视图中声明了哪些变量，就需要在data里面注册，并且为变量进行初始化赋值
				el: '#app', // 利用元素选择器方式选中app div对象
				data: {
					seen: true
				},
				methods: {
					change: function() {
						this.seen = !this.seen
						console.log(this.seen)
					},
				}
			})
		</script>
	</body>
</html>

```

运行程序，`seen`初始状态下值为`true`，当点击按钮时，会调用`change`方法，`change`方法会改变`seen`的值，将其取反，这样不停点击按钮时，下面的字符会循环显示或消失。

![](/img/20210506234630.png)

### 2.3 v-for循环指令

使用`v-for`指令可以循环迭代某一对象。

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<ol>
				<!-- 使用v-for指令绑定数组的数据，进行循环迭代 -->
				<li v-for="todo in todos">
					{{ todo.text }}
				</li>
			</ol>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			// 在引用vue.js时，会声明一个全局变量Vue
			// 通过`new Vue`的方式可以获取一个Vue的应用
			// 它会返回一个对象，我们称之为应用对象，如`app`
			// 在`new Vue`时需要注意的时候，需要传入一个对象{}作为参数
			// 这个对象{}有两个非常重要的属性，el和data
			var app = new Vue({
				// el: element 指代元素属性
				// data: 指代码数据属性，用于保存数据。在视图中声明了哪些变量，就需要在data里面注册，并且为变量进行初始化赋值
				el: '#app', // 利用元素选择器方式选中app div对象
				data: {
					todos: [{
							text: '学习 JavaScript'
						},
						{
							text: '学习 Vue'
						},
						{
							text: '整个牛项目'
						}
					]
				},
			})
		</script>
	</body>
</html>

```

此时页面显示如下：

![](/img/20210506235157.png)

些时我们可以在控制通过`app.todos[index].text`来获取`index`索引对象的文本值：

```sh
# 获取索引值为0的文本值
> app.todos[0].text
< "学习 JavaScript"

# 获取索引值为1的文本值
> app.todos[1].text
< "学习 Vue"

# 获取索引值为2的文本值
> app.todos[2].text
< "整个牛项目"

# 添加一个新元素
> app.todos.push({text: "好项目"})
< 4

# 弹出一个元素
> app.todos.pop()
```

`push`和`pop`可以将元素压入到列表中，或从列表中弹出一个元素。

### 2.4 v-on事件监听指令

通过`v-on`指令可以添加一个事件监听器。官方示例给了一个监听点击事件的示例：

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<p>{{ message }}</p>
			<!--
			 @click是v-on:click的简写，监听点击事件,
			 reverseMessage函数与reverseMessage()函数效果一样
			-->
			<button v-on:click="reverseMessage">反转消息</button>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			// 在引用vue.js时，会声明一个全局变量Vue
			// 通过`new Vue`的方式可以获取一个Vue的应用
			// 它会返回一个对象，我们称之为应用对象，如`app`
			// 在`new Vue`时需要注意的时候，需要传入一个对象{}作为参数
			// 这个对象{}有两个非常重要的属性，el和data
			var app = new Vue({
				// el: element 指代元素属性
				// data: 指代码数据属性，用于保存数据。在视图中声明了哪些变量，就需要在data里面注册，并且为变量进行初始化赋值
				el: '#app', // 利用元素选择器方式选中app div对象
				data: {
					message: 'Hello Vue.js!',
				},
				methods: {
					// 字符串反转
					reverseMessage: function() {
						// 注意split和join中间需要指定''分隔符
						this.message = this.message.split('').reverse().join('')
					}
				}
			})
		</script>
	</body>
</html>

```

点击`反转消息`按钮后，`Hello Vue.js!`字符串就会变成`!sj.euV olleH`，再次点击按钮后，字符串会再次反转还原。

可以看到，当我们点击按钮时，会触发`reverseMessage`函数的执行，`reverseMessage`函数将会将`this.message`的值进行反转。

### 2.5 v-model双向绑定指令

`v-model` 指令可以轻松实现表单输入和应用状态之间的双向绑定。官方示例中，通过修改输入框内容，message消息会自动更新。

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<p>{{ message }}</p>
			<!-- v-model指令实现双向绑定 -->
			<input v-model="message"></input>
			<button v-on:click="reverseMessage">反转消息</button>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			// 在引用vue.js时，会声明一个全局变量Vue
			// 通过`new Vue`的方式可以获取一个Vue的应用
			// 它会返回一个对象，我们称之为应用对象，如`app`
			// 在`new Vue`时需要注意的时候，需要传入一个对象{}作为参数
			// 这个对象{}有两个非常重要的属性，el和data
			var app = new Vue({
				// el: element 指代元素属性
				// data: 指代码数据属性，用于保存数据。在视图中声明了哪些变量，就需要在data里面注册，并且为变量进行初始化赋值
				el: '#app', // 利用元素选择器方式选中app div对象
				data: {
					message: 'Hello Vue.js!',
				},
				methods: {
					// 字符串反转
					reverseMessage: function() {
						// 注意split和join中间需要指定''分隔符
						this.message = this.message.split('').reverse().join('')
					}
				}
			})
		</script>
	</body>
</html>

```

我们在上一节示例的基础上，增加代码`<input v-model="message"></input>`，此时，当我们修改输入框中的内容时，上方的消息也会自动变更。点击按钮时，上方的消息以及输入框中的内容都会反转。

## 3. 组件化应用构建

- 组件是可复用的`Vue`实例。
- 一个组件本质上是一个拥有预定义选项的一个`Vue`实例。

创建一个简单的`todo-item`的组件，并应用：

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<ol>
				<!-- 创建一个 todo-item 组件的实例 -->
				<todo-item></todo-item>
				<todo-item></todo-item>
				<todo-item></todo-item>
			</ol>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			// 定义一个Vue组件
			Vue.component('todo-item', {
				template: '<li>这是一个待办项</li>'
			})
			// 在引用vue.js时，会声明一个全局变量Vue
			// 通过`new Vue`的方式可以获取一个Vue的应用
			// 它会返回一个对象，我们称之为应用对象，如`app`
			// 在`new Vue`时需要注意的时候，需要传入一个对象{}作为参数
			// 这个对象{}有两个非常重要的属性，el和data
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
			})
		</script>
	</body>
</html>

```

此时，界面上显示如下：

![](/img/20210507214607.png)

可以看到，为每个待办项渲染同样的文本，各项都是一样的。



如果我们能够从父作用域将数据传递到子组件才好。Vue有这样的功能。我们只需要修改一下组件的定义，并通过`props`参数设置一个自定义的参数列表。然后将参数传递到`template`中。

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<ol>
				<!-- 
				  为每个 todo-item 提供 todo 对象
				  todo 对象是变量，即其内容可以是动态的。
				  官方文档中说需要指定`v-bind:key`,但不指定也可以正常运行
				-->
				<todo-item v-for='item in todolist' v-bind:todo='item' v-bind:key='item.index'></todo-item>
			</ol>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			// 定义一个Vue组件
			Vue.component('todo-item', {
				// props中可以定义多个自定义属性
				props: ['todo'],
				template: '<li>{{ todo.text }}</li>'
			})
			// 在引用vue.js时，会声明一个全局变量Vue
			// 通过`new Vue`的方式可以获取一个Vue的应用
			// 它会返回一个对象，我们称之为应用对象，如`app`
			// 在`new Vue`时需要注意的时候，需要传入一个对象{}作为参数
			// 这个对象{}有两个非常重要的属性，el和data
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					// 待办事项列表
					todolist: [{
							index: 1,
							text: '买菜'
						},
						{
							index: 2,
							text: '买酸奶'
						},
						{
							index: 3,
							text: '买水果'
						},
					]
				}
			})
		</script>
	</body>
</html>

```

此时运行可以看到，页面中显示出不同的待办事项了：

![](/img/20210507223241.png)

在大型应用中，会将整个应用划分为多个组件，以使开发更容易管理。

如：

```html
<div id="app">
  <app-nav></app-nav>
  <app-view>
    <app-sidebar></app-sidebar>
    <app-content></app-content>
  </app-view>
</div>
```

## 4. Vue实例

- 每个Vue应用都是通过用`Vue`函数创建一个新的`Vue`实例开始的。

如：

```javascript
var vm = new Vue({
  // 选项
})
```

变量名`vm`是`ViewModel`的缩写，表示Vue实例。

- 当创建一个 Vue 实例时，你可以传入一个**选项对象**。
- 选项列表可以在 [https://cn.vuejs.org/v2/api/#选项-数据](https://cn.vuejs.org/v2/api/#%E9%80%89%E9%A1%B9-%E6%95%B0%E6%8D%AE) 查看。如`el`、`data`、`methods`、`props`等等。
- 一个 Vue 应用由一个通过 `new Vue` 创建的**根 Vue 实例**，以及可选的嵌套的、可复用的组件树组成。
- 所有的 Vue 组件都是 Vue 实例，并且接受相同的选项对象 (一些根实例特有的选项除外)。
- 当一个 Vue 实例被创建时，它将 `data` 对象中的所有的 property属性 加入到 Vue 的**响应式系统**中。当这些 property属性 的值发生改变时，视图将会产生“响应”，即匹配更新为新的值。当这些数据改变时，视图会进行重渲染。
- 值得注意的是只有当实例被创建时就已经存在于 `data` 中的 property属性 才是**响应式**的。也就是说，没有在`data`中初始化的属性不会动态响应。

### 4.1 特例-对象冻结

- 使用 `Object.freeze()`，这会阻止修改现有的 property属性，也意味着响应系统无法再*追踪*变化。

如我们使用以下示例：

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			a = {{ a }}
			<button v-on:click="a += 1 ">Change it</button>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			var mydata = {
				a: 1
			}
			// 冻结mydata
			// Object.freeze(mydata)

			// 在引用vue.js时，会声明一个全局变量Vue
			// 通过`new Vue`的方式可以获取一个Vue的应用
			// 它会返回一个对象，我们称之为应用对象，如`app`
			// 在`new Vue`时需要注意的时候，需要传入一个对象{}作为参数
			// 这个对象{}有两个非常重要的属性，el和data
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: mydata,
			})
		</script>
	</body>
</html>

```

当注释掉`Object.freeze(mydata)`时，在页面点击`Change it`按钮时，a的值会不断增加1。

当取消`Object.freeze(mydata)`注释后,再次点击按钮。控制台会抛出异常：

`[Vue warn]: Error in v-on handler: "TypeError: Attempted to assign to readonly property."`即禁止对只读属性进行赋值。



### 4.2 Vue实例属性与方法

可以在 [https://cn.vuejs.org/v2/api/#实例-property](https://cn.vuejs.org/v2/api/#%E5%AE%9E%E4%BE%8B-property) 页面查看所有Vue实例属性与方法。他们都是以`$`开头。

如：

- `vm.$data`, Vue 实例观察的数据对象。
- `vm.$el`，Vue 实例使用的根 DOM 元素。
- `vm.$props`，当前组件接收到的 props 对象。Vue 实例代理了对其 props 对象 property 的访问。

![](/img/20210507235620.png)



### 4.3 实例生命周期

- 每个 Vue 实例在被创建时都要经过一系列的初始化过程——例如，需要设置数据监听、编译模板、将实例挂载到 DOM 并在数据变化时更新 DOM 等。同时在这个过程中也会运行一些叫做**生命周期钩子**的函数，这给了用户在不同阶段添加自己的代码的机会。

- Vue钩子函数类似SVN中的`pre-commit`、`post-commit`等，在特定的情形下执行。

官方文档中的生命周期图：

![](https://cn.vuejs.org/images/lifecycle.png)

  我们参考官方视频示例：[生命周期 https://learning.dcloud.io/#/?vid=4](https://learning.dcloud.io/#/?vid=4)

以及[ 详解vue生命周期 https://segmentfault.com/a/1190000011381906](https://segmentfault.com/a/1190000011381906)


编写如下测试代码 [download lifecycle.html](/scripts/vue/lifecycle.html.txt)  (注意，下载时请将文件后缀修改为`.html`)：

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			{{ message }}
			<button @click="destroy">内部销毁</button>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			// 在引用vue.js时，会声明一个全局变量Vue
			// 通过`new Vue`的方式可以获取一个Vue的应用
			// 它会返回一个对象，我们称之为应用对象，如`app`
			// 在`new Vue`时需要注意的时候，需要传入一个对象{}作为参数
			// 这个对象{}有两个非常重要的属性，el和data
			var app = new Vue({
				// 此处的el属性必须保留
				el: '#app',
				data: {
					message: '消息',
				},
				methods: {
					destroy() {
						this.$destroy()
						console.log('after run this.$destroy()');
						//this.$destroy()不会销毁DOM, 需对DOM进行处理
						document.querySelector('#app').remove()
					},
				},
				// 在实例初始化之后，数据观测 (data observer) 和 event/watcher 事件配置之前被调用。
				beforeCreate: function() {
					console.log('beforeCreate')
					console.log('el:', this.$el); // undefined
					console.log('data:', this.$data); // undefined
					console.log('message:', this.message); // undefined
				},
				/* 在实例创建完成后被立即调用。
				在这一步，实例已完成以下的配置：数据观测 (data observer)，属性和方法的运算，watch/event 事件回调。
				然而，挂载阶段还没开始，$el 属性目前不可见。 */
				created: function() {
					console.log('created')
					console.log('el:', this.$el); // undefined
					console.log('data:', this.$data); // 已经被初始化
					console.log('message:', this.message); // 已经被初始化
				},
				// 在挂载开始之前被调用：相关的渲染函数首次被调用
				beforeMount: function() {
					console.log('beforeMount');
					console.log('el:', this.$el); // 已经被初始化，此时el中通过{{message}}进行占位的
					console.log('data:', this.$data); // 已经被初始化
					console.log('message:', this.message); // 已经被初始化
				},
				//el 被新创建的 vm.$el 替换, 挂载成功	
				mounted: function() {
					console.log('mounted');
					console.log('el:', this.$el); // 已经被初始化，此时el中的{{message}}占位已经被替换成真实的值
					console.log('data:', this.$data); // 已经被初始化
					console.log('message:', this.message); // 已经被初始化
				},
				// 数据更新时调用
				beforeUpdate: function() {
					console.log('beforeUpdate');
					console.log('el:', this.$el); // 已经被更新
					console.log('data:', this.$data); // 已经被更新
					console.log('message:', this.message); // 已经被更新
				},
				// 组件 DOM 已经更新, 组件更新完毕 
				updated: function() {
					console.log('updated');
					console.log('el:', this.$el); // 已经被更新
					console.log('data:', this.$data); // 已经被更新
					console.log('message:', this.message); // 已经被更新
				},
				// 销毁前
				beforeDestroy: function() {
					console.log('beforeDestroy');
					console.log('el:', this.$el); // 数据被保留
					console.log('data:', this.$data); // 数据被保留
					console.log('message:', this.message); // 数据被保留
				},
				// 销毁后
				destroyed: function() {
					console.log('destroyed');
					console.log('el:', this.$el); // 内部销毁时数据被保留
					console.log('data:', this.$data); // 内部销毁时数据被保留
					console.log('message:', this.message); // 内部销毁时数据被保留
				}
			});
		</script>
	</body>
</html>

```

运行代码，在浏览器中打开页面，并查看控制台输出：

![](/img/20210508230633.png)

可以看到，在我们定义了多个钩子函数后，刚开始只执行了4个钩子函数，依次是：

- `beforeCreate`
- `created`
- `beforeMount`
- `mounted`

可以看到：

- 在`beforeCreate`钩子函数执行时，`el`、`data`、`message`都是未定义的，此时我们观测的数据都是空的。
- 在`beforeCreate`和`created`之间的生命周期阶段，`el`仍然是未定义的，`data`、`message`已经有数据了，说明此阶段已经与data属性进行了绑定。el选项还没有。
- 在`created`和`beforeMount`之间的生命周期阶段，由于我们有定义`el: '#app'`属性，此时会继续向下编译。`el`开始有数据了，`data`、`message`数据保持不变，此时el中通过{{message}}进行占位的。因为此时还没有挂载到页面上，还是JavaScript中的虚拟DOM形式存在的。
- 在`beforeMount`和`mounted`之间的生命周期阶段，由于我们有定义`el: '#app'`属性，此时会继续向下编译。`el`开始有数据了，`data`、`message`数据保持不变，此时el中的{{message}}占位已经被data中的message值所替换。页面挂载成功。

注意一点，在`created`和`beforeMount`之间的生命周期阶段，需要对`el`属性和`template`属性进行判断。现阶段我不了解`template`属性，先不展开。

如果我们没有定义`el`属性，会怎么样。我们把代码中的`el: '#app',`行注释掉，再看看控制台输出。

![](/img/20210508233321.png)

此时可以看到，只执行了`beforeCreate`和`created`勾子函数。没有执行后面其他的钩子函数。

此时，如果我们在控制台进行`el`定义，并执行命令：

```sh
el = '#app'
app.$mount(el)
```

此时可以看到执行了后续的`beforeMount`和`mounted`钩子函数，页面被挂载成功。

![](/img/20210508234436.png)

我们把代码中的`el: '#app',`行取消注释。



尝试更新`message`数据。

在控制台执行命令：

```sh
app.message = '新消息'
```



当我们在控制台更新`message`消息后，执行了以下钩子函数：

- `beforeUpdate`
- `updated`

![](/img/20210508235029.png)

可以看到，在`beforeUpdate`钩子执行过程中`el`、`data`中的`message`值已经更新为新的值`新消息`了。在`updated`钩子执行完成后，自动返回了新的消息值。



另外，在销毁实例时，也会调用`beforeDestroy`和`destroyed`钩子函数，在我们点击`内部销毁`按钮时，会调用这两个钩子函数。

![](/img/20210509004532.png)

页面中虽然已经不能看到实例对象了，但数据仍然存在。



参考：

- [生命周期图示](https://cn.vuejs.org/v2/guide/instance.html#生命周期图示)

- [详解vue生命周期](https://segmentfault.com/a/1190000011381906)

- [vue生命周期实战（四）—— 实例销毁](https://blog.csdn.net/jcyka/article/details/106420889)






