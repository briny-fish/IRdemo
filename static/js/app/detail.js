$(function(){
  //获取url中的参数
  function getUrlParam(name) {
   var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
   var r = window.location.search.substr(1).match(reg); //匹配目标参数
   if (r != null && name == 'id') {
      return unescape(r[2]); 
    }
    return null; //返回参数值
  }

    var getItemHtml = function (item, i) {

        return ['<li>',
            '<div class="li-content">',
            ' <a href=' + '"detail?id='+ item.appnum + '&type=' + item.type + '" target="_blank" class="title">',
            item.title,
            ' </a>',
            ' <div class="meta">',
            '   <span class="author">',
            item.applicant,
            '   </span><span style="font-size:12px;">&nbsp;&nbsp;|相关度：</span>',
             '   <span class="type">',
            item.score,
            '   </span><span style="font-size:12px;">&nbsp;&nbsp;|IPC主分类：</span>',
            '   <span class="type">',
            item.ipcmain,
            '   </span><span style="font-size:12px;">&nbsp;&nbsp;|申请号：</span>',
            '   <span class="updateTime">',
            item.appnum,
            '   </span><span style="font-size:12px;">&nbsp;&nbsp;|申请日期：</span>',
            '   <span class="updateTime">',
            item.appdata,
            '   </span>',
            ' </div>',
            ' <p id="textContent-' + i + '" class="textContent">',
            // item.textContent,
            findKeyText(item.abstract, i),
            ' </p>',
            '</div>',
            '</li>'].join('');
    };
  var getHeaderHtml = function (item) {
    return [
      '<h1 class="post-title">',
        item.title,
      '</h1>',
      '<div class="post-meta">',
      ' <span class="author">申请人：',
        item.applicant,
      ' &nbsp;&nbsp;|&nbsp;&nbsp;<span class="type">代理机构：',
        item.Agency,
        ' &nbsp;&nbsp;|&nbsp;&nbsp;<span class="type">ipc主分类：',
        item.ipcmain,
      ' </span>&nbsp;&nbsp;|&nbsp;&nbsp;<span class="type">申请日期：',
        item.appdata,
      ' </span>&nbsp;&nbsp;|&nbsp;&nbsp;<span class="type">申请号：',
        item.appnum,
      ' </span>',
      '</div>'].join('');
  };
  
  var getBodyHtml = function (p) {
    return [
      '<h2>摘要</h2><p>',
        p, 
      '</p>'].join('');
  };
    var getReqHtml = function (p) {
    return [
      '<h2>权利要求</h2><div>',
        p,
      '</div>'].join('');
  };
   
  var html_404 = function() {
    return [
      '  <div class="image"></div>',
      '  <h3 class="title">',
           '未找到您查询的内容',
      '  </h3>',
      '  <div class="oper">',
      '    <p><a href="javascript:history.go(-1)">返回上一级页面></a></p>',
      '    <p><a href="/">回到网站首页></a></p>',
      '  </div>'].join('');
  };

  var id = getUrlParam('id'),
    type = getUrlParam('type'),
    $headerHtml = $('#header'),
    $postHeader = $('#post-header'),
    $postBody = $('#post-body');
    $postReq = $('#post-req');
    $list = $('#list');
  $.ajax({
    type:'get',
    url:'/text',
    data: {
      'id': id,
      'type': type
    },
    success: function(res, status){
      if(res.code == 200) {
        $.each(res.data, function(val) {
          var headerHtml = [];
          var bodyHtml = "";
          var reqHtml = "";
          headerHtml.push(getHeaderHtml(res.data));
          $postHeader.html(headerHtml.join(''));
          // 文章段落循还渲染
          var text_content = [];
          bodyHtml = getBodyHtml(res.data.abstract);
          reqHtml = getReqHtml(res.data.requirement);
          $postBody.html(bodyHtml);
          $postReq.html(reqHtml);
        });
      }else if(res.code == 404) {
        var html = [];
        $('.container').css("display",'none');
        $('.info_404').css("display",'block');
        html.push(html_404());
        $('.info_404').html(html.join(''));
      }
    },
    error: function(res) {
      console.log(res.statusText);
    }
  })


    findKeyText = function(item, i) {
        var textContent = $('#textContent-' + i),
            text = item.replace('\r\n', '');

        return text.substr(0,200);
    }
 $.ajax({
    type:'get',
    url:'/recom',
    data: {
      'id': id
    },
    success: function(res, status){
      if(res.code == 200) {
        var html = [];
                        renderItems = res.textList;
                    for(var i = 0; i <renderItems.length ; i++) {
                        html.push(getItemHtml(renderItems[i], i));
                    }
                    console.log(html);
                    $list.html(html.join(''));
      }
    },
    error: function(res) {
      console.log(res.statusText);
    }
  })})