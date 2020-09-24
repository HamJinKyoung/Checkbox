# Myproject: Checkbox 활용하기

체크박스를 선택할 때마다 선택된 모든 옵션명과 옵션가격의 총합을 그 페이지에서 실시간으로 보여주고, 최종적으로 선택된 옵션의 정보를 DB에 저장하는 프로젝트

체크박스로 값을 넘겨줄 때는 value가 넘어가는데 옵션명과 옵션가격을 동시에 value에 넣을 수가 없어(여러개의 value를 넘길 수가 없어서) javascript의 parent()와 children()을 이용해 값을 가져왔다.

1. models.py

```python
from django.db import models

# Create your models here.
class Option(models.Model):
    def __str__(self):
        return self.option_name

    option_name = models.CharField(max_length=200)
    option_price = models.IntegerField()

class Basket(models.Model):
    ototal_price = models.IntegerField()
    option_list = models.CharField(max_length=200)
```

프로젝트에 필요한 모델을 만들어준다.
Option에는 옵션명을 저장할 option_name과 옵션가격을 저장할 option_price가 있고,
Basket에은 선택한 옵션의 옵션명들을 저장할 option_list와 옵션가격의 총합을 저장할 ototal_price가 있다.

2. index.html

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />

        <title>myproject</title>
    </head>
    <body>
        <h1>체크박스로 옵션을 선택하면 선택한 옵션과 옵션포함 총가격을 보여줘보자!</h1>

        <form method="POST">
            {% csrf_token %}
            <table>
                {% for option in options.all %}
                <tr>
                    <td id="option_name">{{ option.option_name }}</td>
                    <td id="option_price">{{ option.option_price }}원</td>
                    <td><input type="checkbox" class="optioncheckbox" value="{{ option.id }}" /></td>
                </tr>
                {% endfor %}
            </table>
            <label for="optionnames">선택한 옵션: </label>
            <input type="text" name="optionlist" id="optionnames" />
            <label for="ototal">가격: </label>
            <input type="text" name="ototal" id="ototal" />
            <input type="submit" value="담기" onclick="return alert('선택한 옵션을 바구니에 담았습니다!! 바구니를 확인해주세요 :)')" />
        </form>

        <!-- 실시간으로 선택된 값을 보여주기위한 script 넣을 자리-->
    </body>
</html>
```

3. script

```js
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
    $(document).ready(function () {
        $(".optioncheckbox").click(function () {
            var txt = "";   # 옵션명들을 저장할 변수
            var price = 0;  # 옵션가격의 합을 저장할 변수
            $(".optioncheckbox:checked").each(function () {
                var tr = $(this).parent().parent();
                var td = tr.children();
                var option_name = td.eq(0).text();
                var option_price = parseInt(td.eq(1).text());
                txt += option_name+",";
                price += option_price;
            });
            txt = txt.substring(0, txt.length - 1);
            $("#optionnames").val(txt);
            $("#ototal").val(price);
        });
    });
</script>
```

`class=optioncheckbox`인 체크박스를 클릭했을 때 실행하는 함수:

```js
$(".optioncheckbox").click(function () {});
```

선택된 체크박스들(:checked)을 하나씩 가져와서 옵션명과 옵션가격을 저장한다.

```js
$(".optioncheckbox:checked").each(function () {
    var tr = $(this).parent().parent();
    var td = tr.children();
    var option_name = td.eq(0).text();
    var option_price = parseInt(td.eq(1).text());
    txt += option_name + ",";
    price += option_price;
});
```

html에 다음과 같이 되어있으므로

```html
<tr>
    <td id="option_name">{{ option.option_name }}</td>
    <td id="option_price">{{ option.option_price }}원</td>
    <td><input type="checkbox" class="optioncheckbox" value="{{ option.id }}" /></td>
</tr>
```

`$(this).parent().parent()`는 체크박스의 부모(=td)의 부모(=tr)이고,
`tr.children()`는 tr의 자식을 가리키므로 td가 된다.
`td.eq(0).text()`를 하면 td의 0번째에 있는 text, 즉 옵션명을 가져올 수 있고, 마찬가지로 `td.eq(1).text()`로 옵션가격(1번째 td)을 가져올 수 있다.
그런데 옵션가격은 text가 아닌 int로 바꿔서 계산해야 하기 때문에 parseInt()를 이용해 형변환을 해주었다.

4. views.py

```python
from django.shortcuts import render
from myapp.models import Option, Basket

# Create your views here.
def index(request):
    options = Option.objects
    if request.method=='POST':
        if request.POST['optionlist']:
            basket=Basket()
            basket.option_list = request.POST['optionlist']
            basket.ototal_price = request.POST['ototal']
            basket.save()
            return render(request, 'index.html', {'options':options})
    else:
        return render(request, 'index.html', {'options':options})
```

먼저 Option, Basket 모델을 import해주고, options 변수에 Option 객체들을 대입하고 render()를 통해 options를 함께 넘겨준다.
그래야 index.html에서 options를 받아서 옵션을 보여줄 수 있다.
request.method가 POST이고, optionlist에 값이 있으면 basket을 만들어 option_list와 ototal_price를 저장한다.
