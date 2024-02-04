# 事件处理

我们在 [v-on事件监听指令](./vue_basic_use.md#_2-4-v-on事件监听指令)中已经使用`v-on`来监听事件。

- 可以用 `v-on` 指令监听 DOM 事件，并在触发时运行一些 JavaScript 代码。如`<button v-on:click="counter += 1">Add 1</button>`。
- 当事件逻辑比较复杂时，不应将JavaScript代码写在`v-on`指令中，应通过定义方法，并在`v-on`指令中调用方法。
- 调用方法时，可以给方法传递一个参数，如` <button v-on:click="say('what')">Say what</button>`。



## 1.  事件修饰符

> Vue.js 为 `v-on` 提供了**事件修饰符**。之前提过，修饰符是由点开头的指令后缀来表示的。
>
> - `.stop`
> - `.prevent`
> - `.capture`
> - `.self`
> - `.once`
> - `.passive`

```html
<!-- 阻止单击事件继续传播 -->
<a v-on:click.stop="doThis"></a>

<!-- 提交事件不再重载页面 -->
<form v-on:submit.prevent="onSubmit"></form>

<!-- 修饰符可以串联 -->
<a v-on:click.stop.prevent="doThat"></a>

<!-- 只有修饰符 -->
<form v-on:submit.prevent></form>

<!-- 添加事件监听器时使用事件捕获模式 -->
<!-- 即内部元素触发的事件先在此处理，然后才交由内部元素进行处理 -->
<div v-on:click.capture="doThis">...</div>

<!-- 只当在 event.target 是当前元素自身时触发处理函数 -->
<!-- 即事件不是从内部元素触发的 -->
<div v-on:click.self="doThat">...</div>
```

我们曾在 [修饰符](./syntax.md#_2-3-%E4%BF%AE%E9%A5%B0%E7%AC%A6) 中使用`.stop`修饰符阻止单击事件继续传播。



## 2. 按键修饰符



Vue 允许为 `v-on` 在监听键盘事件时添加按键修饰符。

下面我们来测试一下官方给的示例：

```html
<!DOCTYPE html>
<!-- events.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>事件处理</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
      <!-- 只有在 `key` 是 `Enter` 时调用 `vm.submit()` -->
      <label>用户名：</label><input v-on:keyup.enter="submit" v-model="username">
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					username: '',
				},
				methods:{
					submit: function() {
						console.log('submit method.')
						alert('你输入的用户名为:' + this.username)
					},
				}
			})
		</script>
	</body>
</html>

```

这个示例中，当我在输入框中输入`mei`时，按Enter回车键，则会自动触发`submit`方法的执行，控制台输出`submit method.`，并且弹出了警告框。

![](/img/20210616194115.png)

你可以直接将 [`KeyboardEvent.key`](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/key/Key_Values) 暴露的任意有效按键名转换为 kebab-case 来作为修饰符。

```
<input v-on:keyup.page-down="onPageDown">
```

在上述示例中，处理函数只会在 `$event.key` 等于 `PageDown` 时被调用。

## 3. 系统修饰符

可以用如下修饰符来实现仅在按下相应按键时才触发鼠标或键盘事件的监听器。

- `.ctrl`
- `.alt`
- `.shift`
- `.meta`

注意：在 Mac 系统键盘上，meta 对应 command 键 (⌘)。在 Windows 系统键盘 meta 对应 Windows 徽标键 (⊞)。

如:

```html
<!-- Alt + C -->
<input v-on:keyup.alt.67="clear">

<!-- Ctrl + Click -->
<div v-on:click.ctrl="doSomething">Do something</div>
```

其他示例请参考 [https://cn.vuejs.org/v2/guide/events.html](https://cn.vuejs.org/v2/guide/events.html)。