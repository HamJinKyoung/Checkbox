# Checkbox

장고에서 선택된 체크박스의 값을 DB에 저장하는 법

체크박스를 통해 선택한 coursename을 Checkbox 모델에 저장해보는 실습

1. models.py

```python
from django.db import models

class Checkbox(models.Model):
    coursename = models.CharField(max_length=100)
```

선택된 coursename을 저장할 Checkbox 모델을 만들어준다.

1. html

```html
<form method="POST">
    {% csrf_token %}
    <span>Courses: </span>
    <input type="checkbox" value="Python" class="chk" />Python <input type="checkbox" value="Js" class="chk" />Js <input type="checkbox" value="Django" class="chk" />Django
    <hr />
    <input type="text" name="coursename" id="txtvalues" />
    <input id="btn" type="submit" value="저장" onclick="return alert('저장완료!!')" />
</form>
```

form에 input type="checkbox"를 통해 체크박스를 만들어주고,
이때 value는 저장할 값을 적어주면 된다. class, id는 아래 script에서 사용할 것이다.
`onclick="return alert('저장완료!!')"`는 버튼이 클릭되었을 때 alert 메시지를 띄워준다.

2. script

```js
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

<script>
    $(document).ready(function () {
        $(".chk").click(function () {
            var txt = "";
            $(".chk:checked").each(function () {
                txt += $(this).val() + ",";
            });
            txt = txt.substring(0, txt.length - 1);
            $("#txtvalues").val(txt);
        });
    });
</script>
```

체크박스를 선택하면 체크박스 밑에 있는 text 부분에 선택한 coursename들을 실시간으로 보여주기 위한 것이다.

```js
$(".chk").click(function () {}
```

class 이름이 chk인 것이 클릭되었을 때 실행되는 함수

```js
$(".chk:checked").each(function () {
    txt += $(this).val() + ",";
}
```

선택된 .chk의 value 값들을 하나씩 txt 변수에 넣어준다.

```js
$("#txtvalues").val(txt);
```

id가 txtvalues인 곳에 value로 txt 변수에 있는 값을 넣어준다.

3. views.py

```python
from app.models import Checkbox

def savevalues(request):
    if request.method=='POST':
        if request.POST.get('coursename'):
            savedata=Checkbox()
            savedata.coursename = request.POST.get('coursename')
            savedata.save()
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')
```

맨 윗줄에 models.py에 있는 CheckBox를 import 해주고,
savevalues라는 함수를 만들어 POST form으로 받아온 coursename을 Checkbox모델에 저장한다.
이때 request.POST.get('coursename')에 있는 'coursename'은 html에서 `<input type="text" name="coursename" id="txtvalues" />`
이 부분에 있는 name="coursename"이다.

### 참고한 자료

https://www.youtube.com/watch?v=45SB_iI3aZc
