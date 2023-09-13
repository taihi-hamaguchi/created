from django.db import models

#accountsアプリのmodelsモデルからCustomUserをインポート
from accounts.models import CustomUser

class Category(models.Model):
    '''投稿する写真のカテゴリを管理するモデル
    '''
    #カテゴリ名のフィールド
    title=models.CharField(
        verbose_name='カテゴリ', #フィールドのタイトル
        max_length=20)
    
    def __str__(self):
        '''オブジェクトを文字列に変換して返す
        Returns(str):カテゴリ名
        '''
        return self.title

class PhotoPost(models.Model):
    '''投資されたデータを管理するモデル
    '''
    #CustomUserモデル(のuser_id)とPhotoPostモデルを
    #1対多の関係で結び付ける
    #CustomUserが親でPhotoPostが子の関係となる
    user=models.ForeignKey(
        CustomUser,
        #フィードのタイトル
        verbose_name='ユーザー',
        #ユーザーを削除する場合はそのユーザーの投稿データもすべて削除する
        on_delete=models.CASCADE
        )
    #Categoryモデル(のuser_id)とPhotoPostモデルを
    #1対多の関係で結び付ける
    #Categoryが親でPhotoPostが子の関係となる
    category=models.ForeignKey(
        Category,
        #フィードのタイトル
        verbose_name='カテゴリ',
        
        on_delete=models.PROTECT
        )
    
    #タイトル用のフィールド
    title=models.CharField(
        verbose_name='タイトル',
        max_length=200
        )
    
    #コメント用のフィールド
    comment=models.TextField(
        verbose_name='コメント',
        )
    
    #イメージのフィールド1
    image1=models.ImageField(
        verbose_name='イメージ1',
        upload_to='photos'
        )
    
    #イメージのフィールド2
    image2=models.ImageField(
        verbose_name='イメージ2',
        upload_to='photos',
        blank=True,
        null=True
        )
    
    #投稿日時のフィールド
    posted_at=models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
        )
    
    def __str__(self):
        return self.title