from django.shortcuts import redirect, render
from django.http import JsonResponse

def index(request):
    if request.user.is_authenticated:
        # 추후 메인 페이지로 경로 수정 필요
        return redirect("/main")
    else:
        return redirect('users:login')

def health_check(request):
    return JsonResponse({'status': 'ok'})

def main(request):
    return render(request, 'main.html')