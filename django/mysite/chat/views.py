from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("""
Hello, world. You're at the polls index.<br>
한글 적용
<body>
  <h1>입력 필드를 만든다</h1>
  <input>
  <input>
</body>

<form method="POST" class="post-form" enctype="multipart/form-data" action="">
          {%csrf_token%}
          <div class="hr-sect">Profile_update</div>
          <br>
          <div class="form-group">
            <label for="formGroupExampleInput">이메일</label>
            <input type="email" name="user-username" class="form-control" maxlength="50" id="id_user-username" disabled>
          </div>
          <div class="form-group">
            <label for="formGroupExampleInput">비밀번호</label>
            <input type="password" name="user-password1" class="form-control" required id="id_user-password1">
          </div>
          <div class="form-group">
            <label for="formGroupExampleInput">비밀번호 확인</label>
            <input type="password" name="user-password2" class="form-control" required id="id_user-password2">
          </div>
          <div class="form-group">
            <label for="formGroupExampleInput">이름</label>
            <input type="text" name="profile-nick" class="form-control" autofocus required id="id_profile-nick">
          </div>
          <div class="row">
            <div class="col-md-4 mb-3">
              <label for="country">년도</label>
              <select class="custom-select d-block w-100" name="year" id="year" title="년도" required>
              </select>
            </div>
            <div class="col-md-4 mb-3">
              <label for="state">월</label>
              <select class="custom-select d-block w-100" name="month" id="month" title="월" required>
              </select>
            </div>
            <div class="col-md-4 mb-3">
              <label for="zip">일</label>
              <select class="custom-select d-block w-100" name="day" id="day" title="일" required>
              </select>
            </div>
          </div>
          <br>
          <button class="btn btn-lg btn-info btn-block" type="submit">Update Profile</button>
        </form>
""")
