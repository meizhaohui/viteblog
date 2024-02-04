# 计算属性与侦听器

[[toc]]

## 1. 计算属性缓存与方法

我们在前面的章节中 [使用javascript表达式](./syntax.md#_1-4-使用javascript表达式) 中已经使用过以下代码：

```html
{{ message.split('').reverse().join('') }}
```

来对消息进行反转操作。



模板内的表达式非常便利，但是设计它们的初衷是用于简单运算的。在模板中放入太多的逻辑会让模板过重且难以维护。

在这个地方，模板不再是简单的声明式逻辑。你必须看一段时间才能意识到，这里是想要显示变量 `message` 的翻转字符串。当你想要在模板中的多处包含此翻转字符串时，就会更加难以处理。

所以，对于任何复杂逻辑，你都应当使用**计算属性**。

我们测试一下。

```html
<!DOCTYPE html>
<!-- computed.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>计算属性和侦听器的使用</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app" style="margin-left: 100px;">
			<p>原始消息:"{{ message }}"</p>
			<p>直接在模板中使用JavaScript表达式反转消息:"{{ message.split('').reverse().join('') }}"</p>
			<p>1计算属性反转消息:"{{ reversedMessage }}"</p>
			<p>2计算属性反转消息:"{{ reversedMessage }}"</p>
			<p>3计算属性反转消息:"{{ reversedMessage }}"</p>
			<p>1方法反转消息:"{{ reversedMsg() }}"</p>
			<p>2方法反转消息:"{{ reversedMsg() }}"</p>
			<p>3方法反转消息:"{{ reversedMsg() }}"</p>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					message: 'Hello,Vue.js!',
				},
				computed: {
					reversedMessage: function() {
						console.log('reversedMessage计算属性反转消息')
						return this.message.split('').reverse().join('')
					},
				},
				methods: {
					reversedMsg: function() {
						console.log('reversedMsg方法反转消息')
						return this.message.split('').reverse().join('')
					},
				}
			})
		</script>
	</body>
</html>

```

我们在浏览器中打开页面，并打开控制台。

![](/img/20210516235541.png)

可以看到，多次使用计算属性反转消息时，计算属性只执行了一次函数；而使用方法反转消息时，每次都会重新执行一次方法函数，存在重复计算。

当我们在控制台将消息重新赋值时，也可以看到计算属性只执行了一次，而通过方法反转消息则执行了三次。

![](/img/20210517000025.png)

两种方式的最终结果确实是完全相同的。然而，不同的是**计算属性是基于它们的响应式依赖进行缓存的**。只在相关响应式依赖发生改变时它们才会重新求值。这就意味着只要 `message` 还没有发生改变，多次访问 `reversedMessage` 计算属性会立即返回之前的计算结果，而不必再次执行函数。

相比之下，每当触发重新渲染时，调用方法将**总会**再次执行函数。

这就说明计算属性存在缓存机制。

::: tip 提示

我们为什么需要缓存？假设我们有一个性能开销比较大的计算属性 **A**，它需要遍历一个巨大的数组并做大量的计算。然后我们可能有其他的计算属性依赖于 **A**。如果没有缓存，我们将不可避免的多次执行 **A** 的 getter！如果你不希望有缓存，请用方法来替代。

:::



现在我们来模拟一个需要较长时间的程序，看看两者之间的区别：

```html
<!DOCTYPE html>
<!-- computed.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>计算属性和侦听器的使用</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app" style="margin-left: 100px;">
			<p>原始消息:"{{ message }}"</p>
			<p>直接在模板中使用JavaScript表达式反转消息:"{{ message.split('').reverse().join('') }}"</p>
			<p>1计算属性反转消息:"{{ reversedMessage }}"</p>
			<p>2计算属性反转消息:"{{ reversedMessage }}"</p>
			<p>3计算属性反转消息:"{{ reversedMessage }}"</p>
		<!-- 	<p>1方法反转消息:"{{ reversedMsg() }}"</p>
			<p>2方法反转消息:"{{ reversedMsg() }}"</p>
			<p>3方法反转消息:"{{ reversedMsg() }}"</p> -->
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			//参数n为休眠时间，单位为毫秒:
			function sleep(n) {
				var start = new Date().getTime();
				//  console.log('休眠前：' + start);
				while (true) {
					if (new Date().getTime() - start > n) {
						break;
					}
				}
				// console.log('休眠后：' + new Date().getTime());
			}

			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					message: 'Hello,Vue.js!',
				},
				computed: {
					reversedMessage: function() {
						console.log('reversedMessage计算属性反转消息')
						console.log(Date())
						sleep(2000);
						console.log(Date())
						return this.message.split('').reverse().join('')
					},
				},
				methods: {
					reversedMsg: function() {
						console.log('reversedMsg方法反转消息')
						console.log(Date())
						sleep(2000);
						console.log(Date())
						return this.message.split('').reverse().join('')
					},
				}
			})
		</script>
	</body>
</html>

```

先把17-19行的方法反转消息注释掉。

此时，在页面上控制台想看输出。

![](/img/20210517001647.png)

可以看到每次最多只需要2秒钟就显示了所有内容。



现在我们注释掉14-16行，并将17-19行的方法反转消息取消注释。再打开页面查看一下消息。

![](/img/20210517001933.png)

此时运行。渲染整个页面，每次至少需要6秒钟时间。比使用计算属性加载页面慢得多。



这也就说明了计算属性有缓存机制，可以加快数据显示。



**如果你不希望有缓存，请用方法来替代。**



总结：

- 计算属性监听的属性，不需要在`data`属性对象中进行定义。

- 如果一个属性是由其他属性计算而来，该属性受多个属性影响时，使用计算属性。

- 如果中间涉及大量计算，需要多次渲染的话，因为计算属性有缓存，此时用计算属性比较好。

- 计算属性初看起来像是一个方法，但事实上又不是方法，而是是一个与data中定义的数据使用相同方法的属性。

  

## 2. 计算属性与侦听属性

可以使用Watcher来对一些属性进行侦听处理。通过`watch`关键字来定义需要监听的属性值。

以下示例比较使用计算属性和侦听属性的使用。

```html
<!DOCTYPE html>
<!-- computed_watch.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>computed计算属性和watch侦听器</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app" style="margin-left: 50px;">
			First name: <input type="text" name="fname" v-model="firstName"><br>
			Last name: <input type="text" name="lname" v-model="lastName"><br>
			<p>Full name C: {{ cfullName }}</p>
			<p>Full name C1: {{ c1fullName }}</p>
			<p>Full name C2: {{ c2fullName }}</p>
			<p>Full name C3: {{ c3fullName }}</p>
			<p>Full name W: {{ wfullName }}</p>
			<p>Full name W1: {{ w1fullName }}</p>
			<p>Full name W2: {{ w2fullName }}</p>
			<p>Full name W3: {{ w3fullName }}</p>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			// 去掉 vue 的 "You are running Vue in development mode" 提示
			Vue.config.productionTip = false
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					firstName: 'Foo',
					lastName: 'Bar',
					wfullName: '',
					w1fullName: '',
					w2fullName: '',
					w3fullName: '',
					// cfullName: '',
					// c1fullName: '',
					// c2fullName: '',
					// c3fullName: '',
				},
				watch: {
					firstName: function(val, oldval) {
						console.log('change at firstName')
						console.log(oldval);
						this.wfullName = val + ' ' + this.lastName
						this.w1fullName = val + ' ' + this.lastName
						this.w2fullName = val + ' ' + this.lastName
						this.w3fullName = val + ' ' + this.lastName
					},
					lastName: function(val) {
						console.log('change at lastName')
						this.wfullName = this.firstName + ' ' + val
					}
				},
				computed: {
					cfullName: function() {
						console.log('change at cfullName')
						return this.firstName + ' ' + this.lastName
					},
					c1fullName: function() {
						console.log('change at c1fullName')
						return this.firstName + ' ' + this.lastName
					},
					c2fullName: function() {
						console.log('change at c2fullName')
						return this.firstName + ' ' + this.lastName
					},
					c3fullName: function() {
						console.log('change at c3fullName')
						return this.firstName + ' ' + this.lastName
					}
				},
			})
		</script>
	</body>
</html>

```

通过该示例我们可以看到，在打开页面时，显示如下：

![](/img/20210525215904.png)

计算属性相关的属性cfullName、c1fullName、c2fullName、c2fullName会自动计算并渲染到页面，而watch侦听器监听的wfullName、w1fullName、w2fullName、w3fullName由于初始状态时会空值，此时渲染为空字符串，watch侦听器此时没有检查到这几个属性的变化。



当我们在Frist name输入框输入一个字符1时，系统监听到firstName发生了变化。触发了相关函数的执行。此时输出如下：

![](/img/20210525220202.png)

此时，可以看到，由于firstName值的变化，调用了一次watch侦听器中firstName定义的函数，只输出了一次'change at firstName'，但却同时影响了wfullName、w1fullName、w2fullName、w3fullName四个属性值的变化。同时，由于firstName的变化，调用了四个计算属性中定义的函数，每个函数都被调用了，此时cfullName、c1fullName、c2fullName、c2fullName也发生相应的变化。

通过该测试我们可以看到：

- watch侦听器在页面初始化时并不会起作用。而computed计算属性在页面初始化时就会进行计算并渲染页面。
- watch只能监听`data`中定义好的属性，如果不定义的话，则会提示类似以下异常：`[Vue warn]: Property or method "lastName" is not defined on the instance but referenced during render. Make sure that this property is reactive, either in the data option, or for class-based components, by initializing the property`。而`computed`计算属性监听的属性是不需要在`data`中定义的。如果定义的话，则提示类似以下异常：`vue.js:634 [Vue warn]: The computed property "cfullName" is already defined in data.`。
- watch侦听器适合处理一个属性影响多个其他属性的情况。如`firstName`会同时影响`wfullName`、`w1fullName`、`w2fullName`、`w3fullName`四个属性值的变化。计算属性适合处理一个属性受多个属性影响的情况。如`cfullName`受`firstName`和`lastName`的影响。



## 3. 计算属性的setter与getter

计算属性默认只有 getter，不过在需要时你也可以提供一个 setter。get是获取的意思，set是设置的意思，也就是用于计算属性的获取和设置。

以下示例是在官方示例上面进行了修改：

```html
<!DOCTYPE html>
<!-- computed_getter_setter.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>computed计算属性的set与get的使用</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app" style="margin-left: 50px;">
			First name: <input type="text" name="fname" v-model="firstName"><br>
			Last name: <input type="text" name="lname" v-model="lastName"><br>
			<p>Full name C: {{ cfullName }}</p>
			<p>Full name C1: {{ c1fullName }}</p>
			<p>Full name C2: {{ c2fullName }}</p>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			// 去掉 vue 的 "You are running Vue in development mode" 提示
			Vue.config.productionTip = false
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					firstName: 'Foo',
					lastName: 'Bar',
					// cfullName: '',
					// c1fullName: '',
					// c2fullName: '',
				},
				computed: {
					// 方式一，通过函数方式定义计算属性
					cfullName: function() {
						console.log('change at cfullName')
						return this.firstName + ' ' + this.lastName
					},
					// 方式一，通过函数方式定义计算属性，另一种写法
					c1fullName() {
						console.log('change at c1fullName')
						return this.firstName + ' ' + this.lastName
					},
					// 方式二，通过对象方式设置set和get方法
					// get对应计算属性的获取
					// set对应计算属性的设置
					c2fullName: {
						// 获取
						get() {
							console.log('get the c2fullName')
							return this.firstName + ' ' + this.lastName
						},
						// 设置
						// 设置时，需要此处函数中定义新值newValue
						set: function(newValue) {
							console.log('set the c2fullName')
							let names = newValue.split(' ')
							this.firstName = names[0]
							this.lastName = names[names.length - 1]
						}
					},

				},
			})
		</script>
	</body>
</html>

```

当我们把49行的`get()`修改一下，改成`get1()`，这时页面会提示以下异常：``vue.js:634 [Vue warn]: Getter is missing for computed property "c2fullName".

![](/img/20210525230452.png)

我们将该处还原，则显示正常。

然后我们在控制台输入`app.c2fullName=’Kobe Bryant‘`:

![](/img/20210525230755.png)

此时，系统自动调用了计算属性的`set`方法，打印了`set the c2fullName`消息，由于`c2fullName`的值进行了重新设置，将会自动影响`firstName`和`lastName`值的变更，由于这两个值发生了变化，相应的触发了`cfullName`和`c1fullName`计算属性的重新计算，同时由于`c2fullName`自己也变化了，需要重新渲染其值，因此会调用其`get`方法。

## 4. 侦听器

官方示例中使用`Lodash`来限制操作频率，调用API接口来演示了`watch`侦听器的使用。

相对复杂。此处不测试。请参考： [https://cn.vuejs.org/v2/guide/computed.html#侦听器](https://cn.vuejs.org/v2/guide/computed.html#%E4%BE%A6%E5%90%AC%E5%99%A8)




参考：

- [vue系列---理解Vue中的computed,watch,methods的区别及源码实现(六)](https://www.cnblogs.com/tugenhua0707/p/11760466.html)
