from django.contrib import admin
from .models import *

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    # 定义要显示的字段,当元祖中包含元祖时，被包含的元祖在页面将会显示在一行
    # fields = (('title','desc'),'content')
    # fields = ('title', 'desc', 'content')
    # 定义不需要显示的字段
    # exclude = ('desc','content')
    # 定义查看所有数据时该表显示的字段
    list_display = ('user','title','desc','content','click_count','is_recommend','category',)
    # 定义可以点击查看详细信息的字段
    list_display_links = ('title',)
    # 定义在列表中可以编辑的字段,设置后会出现save按钮，在页面可以直接编辑
    list_editable = ('click_count',)
    # 定义可以过滤查询的列
    list_filter = ('user','category',)
    # 定义新增和修改页面的显示
    fieldsets = (
        (None,{
            'fields':('user','title','desc','content',)
        }),
        ('高级设置',{
            'classes':('collapse',),
            'fields':('click_count','is_recommend','tag','category')
        }),
    )



admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Article,ArticleAdmin)