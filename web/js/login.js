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
    var url2 = 'https://api2.bitpie.com'
    var url3 = 'https://api1.bitpie.com'
    var win_height = parseInt($(document).height())
    $('body').css({'minHeight':win_height})
    $('.sussess-container').css({'minHeight':win_height})
    var conutry =1;
    function getcountry(type){
      var url;
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
        type:'GET',
        url:url4+'/api/v1/country',
        dataType:'json',
        success:function(data){
          $('.country-box').addClass('on')
        },
        error:function(){
          conutry+=1
          getcountry(conutry)
        }
      })
    }
    $(".input-country-btn").click(function(){
      $('.country-box').addClass('on')
      var data = [{"country_name": "Canada", "country_calling_code": "1", "currency_code": "CAD", "country_code": "CAN"}, {"country_name": "China", "country_calling_code": "86", "currency_code": "CNY", "country_code": "CHN"}, {"country_name": "Germany", "country_calling_code": "49", "currency_code": "EUR", "country_code": "DEU"}, {"country_name": "France", "country_calling_code": "33", "currency_code": "EUR", "country_code": "FRA"}, {"country_name": "United Kingdom", "country_calling_code": "44", "currency_code": "GBP", "country_code": "GBR"}, {"country_name": "Hong Kong", "country_calling_code": "852", "currency_code": "HKD", "country_code": "HKG"}, {"country_name": "Japan", "country_calling_code": "81", "currency_code": "JPY", "country_code": "JA"}, {"country_name": "Macao", "country_calling_code": "853", "currency_code": "MOP", "country_code": "MAC"}, {"country_name": "Taiwan", "country_calling_code": "886", "currency_code": "TWD", "country_code": "TWN"}, {"country_name": "United States of America", "country_calling_code": "1", "currency_code": "USD", "country_code": "USA"}];
      var html = '';
      for(var i=0; i<data.length; i++){
        html += '<div class="country-list" data-num="'+data[i].country_calling_code+'">'+data[i].country_name+'</div>'
      }
      $(".country-list-box").html(html);
      getcountry(conutry)
    });
    $('.close-btn').click(function(){
      $('.country-box').removeClass('on')
    })
  
  
    var getCodeNum = 1
    function getCode (type,lang){
      var country = parseInt($('#country').attr('data-num'))
      var phoneNum = $("#phoneNum").val()
      var url;
      var self = $('#getCode');
      if(type === 1){
        url = url1
      }else if(type === 2){
        url = url2
      }else if(type === 3){
        url = url3
      }else if(type === 4){
        $('#getCode').attr('disabled',false);
        return $.alert({
          title: 'fail',
          content: i18n.login.fail
        });
        return false
      }
      $.ajax({
        type:'POST',
        url:url1,
        dataType:'json',
        data: {
          phone:phoneNum,
          area:country
        },
        success:function(data){
          
          if(data.code === 1000){
            return $.alert({
              title: '提示',
              content: '手机号不正确'
            });
          }
          
          if(data.code === 210){
            return $.alert({
              title: '提示',
              content: '手机已注册'
            });
          }
          if(data.code === 220){
            return $.alert({
              title: '提示',
              content: '手机号码格式错误'
            });
          }
          if(data.code === 260){
            return $.alert({
              title: '提示',
              content: '验证码已发送'
            });
          }
          if(data.code == 503){
            return $.alert({
              title: '提示',
              content: '未知错误'
            });
          }
          var index = 10;
          $('#getCode').addClass('on')
          var interval = setInterval(function(){
  
            if(index<=1) {
              clearInterval(interval);
              $('#getCode').attr('disabled',false);
              self.text(i18n.login.getCode3);
              $('#getCode').removeClass('on')
              return;
            }
            self.html('<span lang="en">'+ i18n.login.getCode3+'，</span>'+index);
            index--;
          },1000);
  
          self.text(i18n.login.getCode2);
        },
        error:function(e){
          $.alert({
            title: '提示',
            content: '网络错误'
          });
        }
      })
    }
    $("#getCode").on("click",function(){
      var country = parseInt($('#country').attr('data-num'))
      var phoneNum = $("#phoneNum").val()
  
      
      var self = $(this);
      self.attr('disabled',true);
      $('#getCode').addClass('on')
      getCode(getCodeNum,lang)
  
    })
    $(".country-list-box").on("click",".country-list",function(){
      var data = $(this).attr('data-num')
      var name = $(this).html()
      $('#country').html(name).attr('data-num',data)
      $('.country-box').removeClass('on')
    })
  
    var recodeNum = 1
    function recode(type,lang){
      var url;
      var area = $('#country').attr('data-num');
      var phone = $('#phoneNum').val();
      var vaildCode = $('#intro3').val();
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
          verification_code:vaildCode
        },
        success:function(data){
          if(data.code === 230){
            $.alert({
              title: '提示',
              content: '验证码无效'
            });
          }
          if(data.code === 240){
            window.location = "/success.html?area="+area+"&phone="+phone
          }
        },
        error:function(){
          $.alert({
            title: '提示',
            content: '未知错误'
          });
        }
      })
    }
    $('.login-btn').click(function(){
  
      recode(recodeNum,lang)
    })
  })