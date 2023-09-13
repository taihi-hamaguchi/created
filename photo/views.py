from typing import Any
from django.db.models.query import QuerySet

from django.forms.models import BaseModelForm
from django.http import HttpResponse

from django.shortcuts import render

from django.views.generic import TemplateView,ListView

#django.views.genericからCreateViewをインポート
from django.views.generic import CreateView
#django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
#forms# モジュールからPhotoPostFormをインポート
from .forms import PhotoPostForm
#method_decoratorをインポート
from django.utils.decorators import method_decorator
#login_requiredをインポート
from django.contrib.auth.decorators import login_required
#modelsモジュールからモデルPhotoPostをインポート
from .models import PhotoPost
#django.views.genericからDetailViewをインポート
from django.views.generic import DetailView
#django.views.genericからDeleteViewをインポート
from django.views.generic import DeleteView



class IndexView(ListView):
    #index.htmlをレンダリング
    template_name = 'index.html'
    #モデルBlogPostのオブジェクトにorder_by()を適用して投稿日時の降順で並び変える
    queryset=PhotoPost.objects.order_by('-posted_at')
    #1ページに表示するレコードの数
    paginate_by=9


#デコレーターにより、CreatePhotoViewへのアクセスはログインユーザーに限定される
#ログイン状態でなければsettings.pyのLOGIN_URLにリダイレクトされる

@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):

    form_class = PhotoPostForm

    template_name = "post_photo.html"

    success_url = reverse_lazy('photo:post_done')

    def form_valid(self, form):

        postdata = form.save(commit=False)

        postdata.user = self.request.user

        postdata.save()

        return super().form_valid(form)


class PostSuccessView(TemplateView):
    '''
    投稿完了ページ
    Attributes:
        template_name: レンダリングするテンプレート
    '''
    #index.htmlをレンダリングする
    template_name = 'post_success.html'


class CategoryView(ListView):
    '''
    カテゴリページのビュー
    
    Attributes:
        template_name: レンダリングするテンプレート
        paginate_by: １ページに表示するレコードの件数'''
    
    #index.htmlをレンダリングする
    template_name='index.html'
    #1ページに表示するレコードの件数
    peginate_by=9

    def get_queryset(self):
        '''
        クエリを実行する
        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドによりクエリを実行する
        
        Returns: クエリによって取得されたレコード
        '''
        #self.kwargsでキーワードの辞書を取得し、categoryキーの値(Categoryテーブルのid)を取得
        category_id = self.kwargs['category']
        #filter(フィールド名=id)で絞り込む
        categories = PhotoPost.objects.filter(category=category_id).order_by('-posted_at')
        #クエリによって取得されたレコードを返す
        return categories
    
class UserView(ListView):
    '''
    ユーザーの投稿一覧ページのビュー
    Attributes:
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコードの件数'''
    #index.htmlをレンダリングする
    template_name='index.html'
    #1ページに表示するレコードの件数
    paginate_by=9

    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = PhotoPost.objects.filter(
            user=user_id).order_by('-posted_at')
        #クエリによって所得されたレコードを返す
        return user_list

class DetailView(DetailView):
    '''詳細ページのビュー
    投稿記事の詳細を表示するのでDetailViewを継承する
    Attributes:
        template_name: レンダリングするテンプレート
        model: モデルのクラス
    '''

    #post.htmlをレンダリングする
    template_name ='detail.html'
    #クラス変数modelにモデルBlogPostを設定
    model = PhotoPost

class MypageView(ListView):
    '''
    マイページのビュー
    Attributes:
        template_name: レンダリングするテンプレート
        model: モデルのクラス
    '''
    #mypage.hemlをレンダリングする
    template_name ='mypage.html'
    paginate_by=9

    def get_queryset(self):
        '''
        クエリを実行する
        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドによりクエリを実行する
        
        Returns: クエリによって取得されたレコード'''

        #現在ログインしているユーザー名はHttpRequest.userに格納されている
        #filter(userフィールド=userオブジェクト)で絞り込む
        queryset = PhotoPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        #クエリによって取得されたレコードを返す
        return queryset
    
class PhotoDeleteView(DeleteView):
    '''
    レコードの削除を行うビュー
    
    Attributes:
        model: モデル
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコードの件数
        success_url: 削除完了後のリダイレクト先のURL'''
    
    #操作の対象はPhotoPostモデル
    model = PhotoPost
    #photo_delete.htmlをレンダリングする
    template_name ='photo_delete.html'
    #処理完了後にマイページにリダイレクト
    success_url = reverse_lazy('photo:mypage')

    def delete(self,request,*args,**kwargs):
        '''
        レコードの削除を行う
        Paramenters:
            self: PhotoDeleteViewオブジェクト
            request: WSGIRequest(HttpRequest)オブジェクト
            args: 引数として渡される辞書(dict)
            kwargs: キーワード付きの辞書(dict)
                {'pk':21}のようにレコードのidが渡される
                
        Returns:
            HttpResponseRedirect(success_url)を返して
            success_urlにリダイレクト'''
        
        #スーパークラスのdelete()を実行
        return super().delete(request,*args,**kwargs)

   