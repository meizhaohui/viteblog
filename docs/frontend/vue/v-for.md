# v-for循环列表渲染

我们可以使用`v-for`指令来基于一个数组或对象来循环渲染一个列表。

- 使用数组来循环：
  - `v-for` 指令需要使用 `item in items` 形式的特殊语法，其中 `items` 是源数据数组，而 `item` 则是被迭代的数组元素的**别名**。
  - 使用列表循环时，`v-for` 还支持一个可选的第二个参数，即当前项的索引。如`v-for="(item, index) in items"`。
- 使用对象来循环：
  - 可以用 `v-for` 来遍历一个对象的 property属性。如`v-for="value in object"`。
  - 可以提供第二个的参数为 property 属性名称 (也就是键名)，如`v-for="(value, name) in object"`。
  - 还可以用第三个参数作为索引，如`v-for="(value, name, index) in object"`。

我们来测试一下官方的示例。



## 1. v-for对数组进行循环处理

```html
<!DOCTYPE html>
<!-- v-for.html -->
<html>
  <head>
    <meta charset="utf-8">
    <title>v-for循环渲染</title>
    <!-- 开发环境版本，包含了有帮助的命令行警告 -->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  </head>
  <body>
    <div id="app">
      <li v-for="item in items" v-bind:key="item.message">
        {{ item.message }}
      </li>
      <button v-on:click="add">Add</button>
    </div>

    <!-- script脚本包裹了一段js代码 -->
    <script>
      var app = new Vue({
        // 此处的el属性必须保留，否则组件无法正常使用
        el: '#app',
        data: {
          items: [{
              message: 'Foo'
            },
            {
              message: 'Bar'
            }
          ]
        },
        methods: {
          add: function() {
              this.items.push({message: "new message"})
          },
        }
      })
    </script>
  </body>
</html>

```

我们运行代码，并在浏览器中打开页面，看到如下页面;

![](/img/20210603213631.png)

我们连接点击两次`Add`按钮，可以发现控制台提示异常：

![](/img/20210603213757.png)

由于我们使用的是`v-bind:key="item.message"`来确定`key`属性，多们多次点击`Add`按钮后，会出现多个key值是`new message`的`<li>`,因此此时我们应该修改一下`key`绑定的值，我们可以使用`index`索引值。

将12行的
```html
<li v-for="item in items" v-bind:key="item.message">
```
改成

```html
<li v-for="(item,index) in items" v-bind:key="index">
```

将13行改成:

```html
{{index+1}}&nbsp;{{ item.message }}
```
然后再刷新页面，并多次点击`Add`按钮。效果如下：

![](/img/20210603214600.png)

此时可以看到，点击多次按钮时，控制台并不会提示更新异常问题。说明使用`index`作为`key`属性是正确的。



## 2. v-for对对象进行循环处理

> 在遍历对象时，会按 `Object.keys()` 的结果遍历，但是**不能**保证它的结果在不同的 JavaScript 引擎下都一致。

我们来测试一下官方代码。

```html
<!DOCTYPE html>
<!-- v-for_object.html -->
<html>
  <head>
    <meta charset="utf-8">
    <title>v-for循环渲染</title>
    <!-- 开发环境版本，包含了有帮助的命令行警告 -->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  </head>
  <body>
    <div id="app" style="margin-left: 50px;">
      <p>直接循环对象的各属性值</p>
      <li v-for="value in object">
        {{ value }}
      </li>

      <p>循环对象的各属性名和属性值</p>
      <div v-for="(value, name) in object">
        {{ name }}: {{ value }}
      </div>

      <p>循环对象的各属性名和属性值，以及索引号</p>
      <div v-for="(value, name, index) in object">
        {{ index }}. {{ name }}: {{ value }}
      </div>
    </div>

    <!-- script脚本包裹了一段js代码 -->
    <script>
      var app = new Vue({
        // 此处的el属性必须保留，否则组件无法正常使用
        el: '#app',
        data: {
          object: {
            title: 'How to do lists in Vue',
            author: 'Jane Doe',
            publishedAt: '2016-04-10'
          }
        },
      })
    </script>
  </body>
</html>

```

在浏览器中打开页面，效果如下图所示：

![](/img/20210603220219.png)

可以看到`Object.keys(app.object)`获取到了一个数组，数组元素是各属性名，如`title`、`author`和`publishedAt`。不能使用`app.object.keys()`来形成数组。

直接对对象进行循环遍历感觉怪怪的。::crying_cat_face:

## 3. 使用v-for模拟豆瓣书单

豆瓣书单长这样：

![](/img/20210603223512.png)

我模拟生成一个简单的书单表格：

```html
<!DOCTYPE html>
<!-- v-for-books.html -->
<html>
  <head>
    <meta charset="utf-8">
    <title>v-for模拟豆瓣书籍列表</title>
    <!-- 开发环境版本，包含了有帮助的命令行警告 -->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  </head>
  <body>
    <div id="app" style="margin-left: 50px;">
      <h3>出版计算机与互联网</h3>
      <!-- 
      border="1" 给表格的每一格，及边框加上1像素的边框
      cellspacing="0" 单元格间距为0
      cellpadding="10" 单元格边距为10px
       -->
      <table border="1" cellspacing="0" cellpadding="10">
        <thead>
          <tr>
            <th>序号</th>
            <th>书名</th>
            <th>作者</th>
            <th>出版时间</th>
            <th>定价</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(book, index) in books" v-bind:key="index">
            <th>{{ index + 1 }}</th>
            <th>{{ book.title }}</th>
            <th>{{ book.author }}</th>
            <th>{{ book.publishedAt }}</th>
            <th>￥{{ book.price }}</th>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- script脚本包裹了一段js代码 -->
    <script>
      var app = new Vue({
        // 此处的el属性必须保留，否则组件无法正常使用
        el: '#app',
        data: {
          books: [{
            title: 'C++ Primer中文版（第5版）',
            author: '[美] Stanley B. Lippman',
            publishedAt: '2013-09',
            price: 25.60
          }, {
            title: '创作者',
            author: '张宁',
            publishedAt: '2021-05',
            price: 39.99
          }, {
            title: '电脑软硬件维修从入门到精通（第2版）',
            author: '王红军 等',
            publishedAt: '2020-04',
            price: 49.00
          }, {
            title: '高性能MySQL（第3版）',
            author: '[美] 施瓦茨（Baron Schwartz）',
            publishedAt: '2013-05',
            price: 8.99
          }, ]
        },
      })
    </script>
  </body>
</html>

```

效果图：

![](/img/20210603223651.png)

相差甚远。

## 4. v-for就地更新策略

> 当 Vue 正在更新使用 `v-for` 渲染的元素列表时，它默认使用“就地更新”的策略。如果数据项的顺序被改变，Vue 将不会移动 DOM 元素来匹配数据项的顺序，而是就地更新每个元素，并且确保它们在每个索引位置正确渲染。这个类似 Vue 1.x 的 `track-by="$index"`。
>
> 这个默认的模式是高效的，但是**只适用于不依赖子组件状态或临时 DOM 状态 (例如：表单输入值) 的列表渲染输出**。

Vue在进行`v-for`渲染时，默认使用就地更新策略。即默认使用已经渲染的元素。直接在已有的DOM上进行复用修改，这样可以带来一定性能上的提升。Vue官方建议尽可能的可`v-for`每一项提供一个唯一的`key`属性，如可以将`index`或`id`之类的属性作为`key`属性。

如：

```html
<div v-for="(item, sindex) in items" v-bind:key="index">
  <!-- 内容 -->
</div>
```

## 5. 数组更新检测

> Vue 将被侦听的数组的变更方法进行了包裹，所以它们也将会触发视图更新。这些被包裹过的方法包括：
>
> - `push()`
> - `pop()`
> - `shift()`
> - `unshift()`
> - `splice()`
> - `sort()`
> - `reverse()`
>
> 你可以打开控制台，然后对前面例子的 `items` 数组尝试调用变更方法。比如 `example1.items.push({ message: 'Baz' })`。

而我们通过 [JavaScript 数组方法](https://www.w3school.com.cn/js/js_array_methods.asp)可以了解到，javascript中数组具有以下方法：

- `toString()`,把数组转换为数组值（逗号分隔）的字符串。
- `join(sep)`,将所有数组元素结合为一个字符串。默认使用逗号作为分隔符，也可以指定wep参数作为分隔符。
- `pop()`，从数组中删除最后一个元素。
- `push(item)`,（在数组结尾处）向数组添加一个新的元素`item`。
- `shift()`,位移与弹出等同，但处理首个元素而不是最后一个。会删除首个数组元素，并把所有其他元素“位移”到更低的索引。，简单理解就是将数组开头元素弹出。
- `unshift()` 方法（在开头）向数组添加新元素，并“反向位移”旧元素，简单理解就是在数组开头插入元素。
- `length`属性，返回数组长度。
- `splice()` 方法可用于向数组添加新项，其接收多个参数，第1个参数定义了应添加新元素的位置（拼接），第2个参数定义要删除几个元素，如果还是其他参数的话，则都是新增元素。
- `concat()` 方法通过合并（连接）现有数组来创建一个新数组,类似于Python中的`list.extend()`。
- `slice() `方法用数组的某个片段切出新数组。它接受两个参数，该方法会从开始参数选取元素，直到结束参数（不包括）为止。如果结束参数被省略，则 `slice()` 会切出数组的剩余部分。
- `reverse() `方法反转数组中的元素。
- `sort() `方法以字母顺序对数组进行排序。



我们使用数组的变化，更新一下书单表格。

```html
<!DOCTYPE html>
<!-- v-for-books.html -->
<html>
  <head>
    <meta charset="utf-8">
    <title>v-for模拟豆瓣书籍列表</title>
    <!-- 开发环境版本，包含了有帮助的命令行警告 -->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>

    <!-- 参考：https://code.z01.com/bootstrap-vue/docs/#browser -->
    <!-- Load required Bootstrap and BootstrapVue CSS -->
    <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap/dist/css/bootstrap.min.css" />
    <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap-vue@latest/dist/bootstrap-vue.min.css" />
    <!-- Load Vue followed by BootstrapVue -->
    <script src="//unpkg.com/vue@latest/dist/vue.min.js"></script>
    <script src="//unpkg.com/bootstrap-vue@latest/dist/bootstrap-vue.min.js"></script>
    <style>
      .active {
        background-color: #c3e6cb;
      }
    </style>
  </head>
  <body>
    <div id="app" style="margin-left: 50px;">
      <h3>出版计算机与互联网</h3>
      <!-- 
      border="1" 给表格的每一格，及边框加上1像素的边框
      cellspacing="0" 单元格间距为0
      cellpadding="10" 单元格边距为10px
       -->
      <table border="1" cellspacing="0" cellpadding="10">
        <thead>
          <tr>
            <th>序号</th>
            <th>书名</th>
            <th>作者</th>
            <th>出版时间</th>
            <th>定价</th>
            <th>动作</th>
          </tr>
        </thead>
        <tbody>
          <!-- v-bind:key="index" -->
          <tr v-for="(book, index) in books" v-bind:class="[index % 2 === 0 ? activeClass: '']">
            <th>{{index + 1}}</th>
            <th><input type="text" style="width: 300px;" v-model="book.title" v-bind:disabled="isDisabledIndex!==index">
            </th>
            <th><input type="text" v-model="book.author" v-bind:disabled="isDisabledIndex!==index"></th>
            <th><input type="text" v-model="book.publishedAt" v-bind:disabled="isDisabledIndex!==index"></th>
            <th><input type="text" v-model="book.price" v-bind:disabled="isDisabledIndex!==index"></th>
            <th>
              <b-button variant="success" v-on:click="addBook(index)">新增</b-button>&nbsp;&nbsp;
              <b-button variant="primary" v-on:click="editBook(index)">{{book.editButtonName}}</b-button>&nbsp;&nbsp;
              <b-button variant="danger" v-on:click="deleteBook(index)">删除</b-button>
            </th>

          </tr>
        </tbody>
      </table>
    </div>

    <!-- script脚本包裹了一段js代码 -->
    <script>
      // 在数组的索引index处插入item元素
      Array.prototype.insert = function(index, item) {
        this.splice(index, 0, item);
      };

      var app = new Vue({
        // 此处的el属性必须保留，否则组件无法正常使用
        el: '#app',
        data: {
          books: [{
            title: 'C++ Primer中文版（第5版）',
            author: '[美] Stanley B. Lippman',
            publishedAt: '2013-09',
            price: 25.60
          }, {
            title: '创作者',
            author: '张宁',
            publishedAt: '2021-05',
            price: 39.99
          }, {
            title: '电脑软硬件维修从入门到精通（第2版）',
            author: '王红军 等',
            publishedAt: '2020-04',
            price: 49.00
          }, {
            title: '高性能MySQL（第3版）',
            author: '[美] 施瓦茨（Baron Schwartz）',
            publishedAt: '2013-05',
            price: 8.99
          }, ],
          activeClass: 'active',
          isDisabledIndex: -1,
        },
        created: function() {
          console.log('created')
          // 给列表中的对象增加属性，便于控制每行的编辑按钮
          for (i = 0; i < this.books.length; i++) {
            this.books[i].editButtonName = '编辑'
            this.books.jo
          }
        },
        methods: {
          deleteBook: function(index) {
            // 删除行
            this.books.splice(index, 1)
          },
          addBook: function(index) {
            // 新增行
            let book = JSON.parse(JSON.stringify(this.books[index]))
            this.books.insert(index, book)
          },
          editBook: function(index) {
            // 编辑行或保存行
            if (this.books[index].editButtonName === '编辑') {
              this.isDisabledIndex = index
              this.books[index].editButtonName = '保存'
            } else {
              this.isDisabledIndex = -1
              this.books[index].editButtonName = '编辑'
            }
          },
        }
      })
    </script>
  </body>
</html>

```

更新后的代码，可以实现书单的新增、编辑、删除和保存功能（注，并没有实际保存到后端去）。效果图如下:

![](/img/20210609231643.png)



如我们在示例中使用了：

- ` this.splice(index, 0, item);`实现元素的插入。
- `this.books.splice(index, 1)`实现元素的删除。

另外，我们在之前的章节 [计算属性与侦听器](./computed_watch.md)中已经使用过`this.message.split('').reverse().join('')`来对数组进行反转和结合。

我们也可以在控制台使用数组的方法来改变我们页面的显示。

![](/img/20210610080953.png)

经过`pop()`和`shift()`操作后，`app.books`的长度变成2了。

你还可以进行其他的方法的测试。此处省略。



## 6. v-for与过滤器联合使用

我们也可以在`v-for`中使用过滤器。如官方示例通过两种方式显示偶数。请看以下代码。

```html
<!DOCTYPE html>
<!-- v_for_filter.html -->
<html>
  <head>
    <meta charset="utf-8">
    <title>v-for中显示过滤/排序后的结果</title>
    <!-- 开发环境版本，包含了有帮助的命令行警告 -->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  </head>
  <body>
    <div id="app">
      <p>通过computed计算属性进行过滤</p>
      <li v-for="n in evenNumbers">{{ n }}</li>
      <p>通过methods方法进行过滤</p>
      <ul v-for="set in sets">
        <li v-for="n in even(set)">{{ n }}</li>
      </ul>
    </div>

    <!-- script脚本包裹了一段js代码 -->
    <script>
      var app = new Vue({
        // 此处的el属性必须保留，否则组件无法正常使用
        el: '#app',
        data: {
          numbers: [1, 2, 3, 4, 5],
          sets: [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10]
          ]
        },
        computed: {
          evenNumbers: function() {
            // javascript数组filter过滤器
            // 参考：https://www.runoob.com/jsref/jsref-filter.html
            // 语法：
            // array.filter(function(currentValue,index,arr), thisValue)
            return this.numbers.filter(function(value, index, arr) {
              return value % 2 === 0
            })
          }
        },
        methods: {
          even: function(numbers) {
            console.log('过滤偶数.')
            return numbers.filter(
              function(value, index, arr) {
                return value % 2 === 0
              }
            )
          },
        }
      })
    </script>
  </body>
</html>

```

运行结果：

![](/img/20210612220706.png)

可以看到通过计算属性或方法的方式都可以进行过滤处理。