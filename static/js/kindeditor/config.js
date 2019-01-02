KindEditor.ready(function(K) {
    window.editor = K.create('#id_content',{

        // 指定大小
        width:'800px',
        height:'200px',
        // 指定上传图片时所请求的路径
        uploadJson: '/admin/upload/kindeditor',
    });
});
