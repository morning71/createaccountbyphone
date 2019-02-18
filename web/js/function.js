function checkPhone(code,str){
    var result = false;
    if(code == "86"){
      if(/^1[0|3|4|5|7|8|9][0-9]\d{8}$/.test(str)){
        result = true;
      }
    }else{
      if(/\d{5,13}/.test(str)){
        result = true;
      }
    }
    return result
  }
  function getlang(){
    var lang = navigator.language||navigator.userLanguage;//常规浏览器语言和IE浏览器
    lang = lang.substr(0, 2);//截取lang前2位字符
    console.log(lang)
    if (lang == 'zh'){
      lang = 'cn';
    }else {
      lang = 'en'
    }
  
    return lang;
  }
  function pageName() {
    var strUrl=location.href;
    var arrUrl=strUrl.split("/");
    var strPage=arrUrl[arrUrl.length-1];
    return strPage;
  }
  function i18npage(pageName){
    var data;
    var lang = getlang()
    var i18n ;
    if(lang === 'cn') {
      i18n = cn
    }else{
      i18n = en
    }
    if(pageName === 'login.html' || pageName === 'login'){
      data = i18n.login
      $('#intro1').html(data.intro1)
      $('#phoneNum').attr('placeholder',data.phoneNum)
      $('#intro3').attr('placeholder',data.intro3)
      $('#account').attr('placeholder',data.account)
      $('#activekey').attr('placeholder',data.activekey)
      $('#ownerkey').attr('placeholder',data.ownerkey)
      $('#title1').html(data.title1)
      $('#title2').html(data.title2)
      $('#title3').html(data.title3)
      $('#title4').html(data.title4)
      $('#title5').html(data.title5)
      $('#title6').html(data.title6)
      $('#getCode').html(data.getCode)
      $('#button').html(data.button)
      $('#buttonlog').html(data.buttonlog)
    }else if(pageName === 'get_reward.html' || pageName === 'get_reward'){
      data = i18n.reward
      $('#button').html(data.button)
      $('#title').html(data.title)
      $('#foot').html(data.foot)
      var html = ''
      for(var i in data.intro){
        html += '<div>' + data.intro[i] + '</div>'
      }
      $('#intro').html(html)
      $('#reward-white').attr('src',data.img)
      $('#reward-banner-img').attr('src',data.banner)
    }else if(pageName === 'success.html' || pageName === 'success'){
      data = i18n.success
      $('#intro').html(data.intro)
      $('#successButton').html(data.button)
      $('#successBg').attr('src',data.successBg)
    }else if(pageName === 'share' || pageName === 'share.html'){
      data = i18n.share
      var html ='';
      for(var i = 0;i<data.intro.length; i++){
        html+= '<div>'+data.intro[i] +'</div>'
      }
      $('#shareBg').attr('src',data.banner)
      $('#share-intro').html(html)
      $('#copy-url').html(data.btn1)
      $('#share').html(data.btn2)
  
    }
  }
  function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
  }
  function system(){
    var u = navigator.userAgent, app = navigator.appVersion;
    var isAndroid = u.indexOf('Android') > -1 || u.indexOf('Linux') > -1; //g
    var isIOS = !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/); //ios终端
    if (isAndroid) {
      return 'android'
    }
    if (isIOS) {
      return 'ios'
    }
  }