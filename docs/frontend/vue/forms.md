# 表单输入绑定

HTML 表单用于收集用户输入。表单元素包括不同类型的 input 元素、复选框、单选按钮、提交按钮等等。

可以使用`v-model`来进行表单元素的双向绑定。

> `v-model` 在内部为不同的输入元素使用不同的 property 并抛出不同的事件：
>
> - text 和 textarea 元素使用 `value` property 和 `input` 事件；
> - checkbox 和 radio 使用 `checked` property 和 `change` 事件；
> - select 字段将 `value` 作为 prop 并将 `change` 作为事件。

`v-model` 会忽略所有表单元素的 `value`、`checked`、`selected` attribute 的初始值而总是将 Vue 实例的数据作为数据来源。你应该通过 JavaScript 在组件的 `data` 选项中声明初始值。

## 1. 单行文本输入

使用以下示例来演示单行文本输入。

```html
<!DOCTYPE html>
<!-- forms.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>表单输入绑定</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
      <input placeholder="edit me" value="message"><br>
      <input v-model="message" placeholder="edit me" value="message"><br>
      <p>Message is: {{ message }}</p>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					message: 'message in data',
				}	
			})
		</script>
	</body>
</html>

```

示例中，上面一个输入框不使用`v-model`进行绑定，指定了`value="message"`，值被直接渲染到输入框中。

而下面一个输入框中使用了`v-model`进行绑定，此时虽然指定了`value="message"`，但被`v-model`忽略，而是使用在`data`属性中声明的初始化值`message in data`，此时输入框中显示的是`message in data`。

![](/img/20210616221833.png)

## 2. 多行文本

我们修改一下代码：

```html
		<div id="app">
      <p>单行文本</p>
      <input placeholder="edit me" value="message"><br>
      <input v-model="message" placeholder="edit me" value="message"><br>
      <p>Message is: {{ message }}</p>
      
      <p>多行文本</p>
      <span>Multiline message is:</span>
      <p style="white-space: pre-line;">{{ message }}</p>
      <br>
      <textarea v-model="message" placeholder="add multiple lines"></textarea>
		</div>
```

可以看到，在多行文本中增加新行后，在单行文本中显示的是一行，而在多行文本中显示的是多行。

![](/img/20210616223008.png)

## 3. 复选框

单个复选框绑定到布尔值。选中为true，未选中为false。

多个复选框则绑定到一个数组。在data属性中指定初始化选中的值。

```html
<!DOCTYPE html>
<!-- forms.html -->
<html>
	<head>
		<meta charset="utf-8">
		<title>表单输入绑定</title>
		<!-- 开发环境版本，包含了有帮助的命令行警告 -->
		<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
      <p>单行文本</p>
      <input placeholder="edit me" value="message"><br>
      <input v-model="message" placeholder="edit me" value="message"><br>
      <p>Message is: {{ message }}</p>
      
      <p>多行文本</p>
      <span>Multiline message is:</span>
      <p style="white-space: pre-line;">{{ message }}</p>
      <br>
      <textarea v-model="message" placeholder="add multiple lines"></textarea>
      
      <p>单个复选框</p>
      <input type="checkbox" id="checkbox" v-model="checked">
      <label for="checkbox">{{ checked }}</label>
      
      <p>多个复选框</p>
      <input type="checkbox" id="jack" value="Jack" v-model="checkedNames">
      <label for="jack">Jack</label>
      <input type="checkbox" id="john" value="John" v-model="checkedNames">
      <label for="john">John</label>
      <input type="checkbox" id="mike" value="Mike" v-model="checkedNames">
      <label for="mike">Mike</label>
      <br>
      <span>Checked names: {{ checkedNames }}</span>
		</div>

		<!-- script脚本包裹了一段js代码 -->
		<script>
			var app = new Vue({
				// 此处的el属性必须保留，否则组件无法正常使用
				el: '#app',
				data: {
					message: 'message in data',
          checked: true,
          checkedNames: ['Mike'], // 初始时选中Mike
				}	
			})
		</script>
	</body>
</html>

```

运行效果如下图:

![](/img/20210616224352.png)

## 4. 单选按钮

测试代码如下:

```html
<!DOCTYPE html>
<!-- forms.html -->
<html>
  <head>
    <meta charset="utf-8">
    <title>表单输入绑定</title>
    <!-- 开发环境版本，包含了有帮助的命令行警告 -->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  </head>
  <body>
    <div id="app">
      <p>单选按钮</p>
      <input type="radio" id="one" value="One" v-model="picked">
      <label for="one">One</label>
      <br>
      <input type="radio" id="two" value="Two" v-model="picked">
      <label for="two">Two</label>
      <br>
      <span>Picked: {{ picked }}</span>
    </div>

    <!-- script脚本包裹了一段js代码 -->
    <script>
      var app = new Vue({
        // 此处的el属性必须保留，否则组件无法正常使用
        el: '#app',
        data: {
          picked: ''
        }
      })
    </script>
  </body>
</html>

```

此时运行效果如下图:

![](/img/20210616230527.png)

只能选中一个，选择`One`或者`Two`。

## 5. 下拉选择框

单选时，绑定到一个具体的值。多选时，绑定到一个数组。

```html
<!DOCTYPE html>
<!-- forms.html -->
<html>
  <head>
    <meta charset="utf-8">
    <title>表单输入绑定</title>
    <!-- 开发环境版本，包含了有帮助的命令行警告 -->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  </head>
  <body>
    <div id="app">
      <p>选择框</p>
      <p>单选</p>
      <select v-model="singleSelected">
        <option disabled value="">请选择</option>
        <option>A</option>
        <option>B</option>
        <option>C</option>
      </select>
      <span>Selected: {{ singleSelected }}</span><br>

      <p>多选</p>
      <select v-model="selected" multiple style="width: 50px;">
        <option>A</option>
        <option>B</option>
        <option>C</option>
      </select>
      <br>
      <span>Selected: {{ selected }}</span>
    </div>

    <!-- script脚本包裹了一段js代码 -->
    <script>
      var app = new Vue({
        // 此处的el属性必须保留，否则组件无法正常使用
        el: '#app',
        data: {
          selected: [],
          singleSelected: '',
        }
      })
    </script>
  </body>
</html>

```

注意，多选时，应将`Ctrl`键或`Shift`键按住，来选择多个。

![](/img/20210616231327.png)

推荐使用Vue-Multiselect来处理下拉选择。请参考[Vue-Multiselect下拉框强化插件的使用](./use_Vue-Multiselect.md) 。



## 6. 修饰符

`v-model`支持以下修饰符：

- `.lazy` 在“change”时而非“input”时更新。lazy修饰符是让数据在失去焦点或者回车时才会更新，避免value内容没有打完就执行后续的方法。
- `.number` 将用户的输入值转为数值类型。
- `.trim` 自动过滤用户输入的首尾空白字符。

### 6.1 `.lazy`修饰符

请看以下示例。

```html
<!DOCTYPE html>
<!-- forms.html -->
<html>
  <head>
    <meta charset="utf-8">
    <title>表单输入绑定</title>
    <!-- 开发环境版本，包含了有帮助的命令行警告 -->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  </head>
  <body>
    <div id="app">
      <p>修饰符的使用</p>
      <p>单行文本</p>
      <input v-model="message" placeholder="edit me"><br>
      <input v-model.lazy="message" placeholder="edit me"><br>
      <p>Message is: {{ message }}</p>
    </div>

    <!-- script脚本包裹了一段js代码 -->
    <script>
      var app = new Vue({
        // 此处的el属性必须保留，否则组件无法正常使用
        el: '#app',
        data: {
          message: 'message in data',
        }
      })
    </script>
  </body>
</html>

```

![](/img/20210616233054.png)

第一个输入框不使用`.lazy`修饰符，则每次输入时一个字符时都会同步更新<p>标签中的显示，并且会更新第二个输入框中的输入内容。

而第二个输入框因为使用了`.lazy`修饰符，则只有当输入框失去焦点或者按回车键时，才进行同步更新数据。

### 6.2 `.number`修饰符

我们看以下示例：

```html
<!DOCTYPE html>
<!-- forms.html -->
<html>
  <head>
    <meta charset="utf-8">
    <title>表单输入绑定</title>
    <!-- 开发环境版本，包含了有帮助的命令行警告 -->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  </head>
  <body>
    <div id="app">
      <p>修饰符的使用</p>
      <input v-model="age" type="number" v-on:change="change">
      <input v-model.number="age" type="number" v-on:change="change">
    </div>

    <!-- script脚本包裹了一段js代码 -->
    <script>
      var app = new Vue({
        // 此处的el属性必须保留，否则组件无法正常使用
        el: '#app',
        data: {
          age: 16,
        },
        methods: {
          change: function() {
            console.log(this.age)
            console.log(typeof(this.age))
          }
        }
      })
    </script>
  </body>
</html>

```

可以看到，修改第一个输入框数值时，输出的类型是`string`字符串类型。而修改第二个输入框数值时，输出的类型是`number`类型。说明使用`.number`修饰符已经将输入的数据自动转换成数值类型了。

![](/img/20210617064500.png)



### 6.3 `.trim`修饰符

我们也可以使用`.trim`修饰符来将用户输入的字符两端的空白字符自动移除。

请看如下示例：

```html
<!DOCTYPE html>
<!-- forms.html -->
<html>
  <head>
    <meta charset="utf-8">
    <title>表单输入绑定</title>
    <!-- 开发环境版本，包含了有帮助的命令行警告 -->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  </head>
  <body>
    <div id="app">
      <p>修饰符的使用</p>
      <input v-model="username" v-on:change="change">
      <input v-model.trim="username" v-on:change="change">
    </div>

    <!-- script脚本包裹了一段js代码 -->
    <script>
      var app = new Vue({
        // 此处的el属性必须保留，否则组件无法正常使用
        el: '#app',
        data: {
          username: '',
        },
        methods: {
          change: function() {
            console.log("用户名:'" + this.username + "'")
          }
        }
      })
    </script>
  </body>
</html>

```

第一个输入框没有使用`.trim`修饰符，当这个输入框输入带有空格的字符"    mei     "时，在控制台输入中可以看到输出：`用户名:'    mei     '`,可以看到包含了字符串前后的空白字符。

![](/img/20210617065454.png)

而我们改变第二个输入框时，在输入框后面再增加一些空格，此时仅输出`mei`。并且可以看到，视图被重新渲染，输入框字符两端的空格被自动移除了，仅保留了`mei`。

![](/img/20210617070002.png)