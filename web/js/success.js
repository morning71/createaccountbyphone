$(function(){
    var lang = getlang()
    var i18n ;
    if(lang === 'cn') {
      i18n = cn
      lang = 'cn'
    }else{
      i18n = en
      lang = 'en'
    }
    var url1 = 'http://192.168.0.171:8349/post'
    var win_height = parseInt($(document).height())
    $('body').css({'minHeight':win_height})
    $('.sussess-container').css({'minHeight':win_height})

    function GetRequest() {
        var url = location.search; //获取url中"?"符后的字串
        var theRequest = new Object();
        if (url.indexOf("?") != -1) {
           var str = url.substr(1);
           strs = str.split("&");
           for(var i = 0; i < strs.length; i ++) {
              theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
           }
        }
        return theRequest;
     }
    var Res = GetRequest();
    var recodeNum = 1
    function recode(type,lang){
      var url;
      var area = Res['area'];
      var phone = Res['phone'];
      var user_name = $('#account').val();
      var active_key = $('#activekey').val();
      var owner_key = $('#ownerkey').val();
      if(type === 1){
        url = url1
      }else if(type === 2){
        url = url2
      }else if(type === 3){
        url = url3
      }else if(type === 4){
        return false
      }
      $.ajax({
        type:'POST',
        url:url1,
        dataType:'json',
        data:{
          area:area,
          phone:phone,
          user_name:user_name,
          active_key:active_key,
          owner_key:owner_key
        },
        success:function(data){
          if(data.code === 320){
            $.alert({
              title: '提示',
              content: '注册成功'
            });
          }
          if(data.code === 330){
            $.alert({
              title: '提示',
              content: '秘钥错误'
            });
          }
          if(data.code === 340){
            $.alert({
              title: '提示',
              content: '用户名格式错误'
            });
          }
          if(data.code === 350){
            $.alert({
              title: '提示',
              content: '用户名已存在'
            });
          }
          if(data.code === 503){
            $.alert({
              title: '提示',
              content: '未知错误'
            });
          }
          
        },
        error:function(){
          $.alert({
            title: '提示',
            content: '网络错误'
          });
        }
      })
    }

    $('#buttonlog').click(function(){
  
      recode(recodeNum,lang)
    })
})