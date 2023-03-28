define(function (require, exports, module) {

    var $ = require('../lib/jquery'),
        Ajax = require('../mod/ajax'),
        PageView = require('../mod/pageView');
var searchMsg = document.getElementById("search-msg");
    var getItemHtml = function (item, i, key) {

        return ['<li>',
            '<div class="li-content">',
            ' <a href=' + '"detail?id='+ item.appnum + '&type=' + item.type + '" target="_blank" class="title">',
            item.title,
            ' </a>',
            ' <div class="meta">',
            '   <span class="author">',
            item.applicant,
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
            findKeyText(item.abstract, i, key),
            ' </p>',
            '</div>',
            '</li>'].join('');
    };

    var html_404 = function() {
        return [
            '  <div class="image"></div>',
            '  <h3 class="title">',
            '未找到您查询的内容',
            '  </h3>',
            '  <div class="oper">',
            '    <p><a href="javascript:history.go(-1)">返回上一级页面></a></p>',
            '    <p><a href="/search">回到网站首页></a></p>',
            '  </div>'].join('');
    };
    var flag = 0;//0 searchall 1 ipc 2 appnum 3 enquery
    var str = window.location.search;//获取url里面的参数
    if (str.indexOf('keyword') != '-1'){
        flag = -1;
        var pos_start = str.indexOf('keyword') + 'keyword'.length + 1;
        var pos_end = str.indexOf("&", pos_start);
        if (pos_end == -1){
            var keyword = decodeURI(str.substring(pos_start));

        }else{
            alert("1!");
        }
    }

    var str = window.location.search;//获取url里面的en query参数
    if (str.indexOf('en') != '-1'){
        flag = 3;
        var pos_start = str.indexOf('en') + 'en'.length + 1;
        var pos_end = str.indexOf("&", pos_start);
        if (pos_end == -1){
            var en = decodeURI(str.substring(pos_start));

        }else{
            alert("1!");
        }
    }


    var str = window.location.search;//获取url里面的参数
    if (str.indexOf('ipc') != '-1'){
        flag = 1;
        var pos_start = str.indexOf('ipc') + 'ipc'.length + 1;
        var pos_end = str.indexOf("&", pos_start);
        if (pos_end == -1){
            var ipc = decodeURI(str.substring(pos_start));

        }else{
            alert("3!");
        }
    }

    var str = window.location.search;//获取url里面的参数
    if (str.indexOf('appnum') != '-1'){
        flag = 2;
        var pos_start = str.indexOf('appnum') + 'appnum'.length + 1;
        var pos_end = str.indexOf("&", pos_start);
        if (pos_end == -1){
            var appnum = decodeURI(str.substring(pos_start));

        }else{
            alert("3!");
        }
    }

    // 数据分页渲染
    getData = function () {
        pageView.disable();
        var data = {};
        if(flag==-1){
            alert('1');
            data.keyword = decodeURI(keyword);//二次encode的URL，需要二次decode
        }
        else if(flag==3){
            console.log('flag==3')
            alert('3');
            data.en = decodeURI(en);//二次encode的URL，需要二次decode
        }
        else if(flag==1){alert('1');console.log('flag==1');data.ipc = decodeURI(ipc);}
        else{alert('2');console.log('flag==2');data.appnum=decodeURI(appnum)}
        data.page = pageView.getParams().page;
        data.page_size = pageView.getParams().page_size;
        if(flag==-1){
        Ajax.get('/searchAll', data)
            .done(function (res) {
                if (res.code == 200) {
                    console.log(res);
                    var total1 = res.total1;
                    var total = res.total;

                    pageView.refresh(total1);
                    var html = [],
                        renderItems = res.textList,
                        num = pageView.pageSize,
                        start = 1,
                        end = num,
                        flag = false;
                    for(var i = start-1; i < end ; i++) {
                        html.push(getItemHtml(renderItems[i], i, keyword));
                    }
                    $result.html("共搜索到 <span style='color:red;'>" + res.total + "</span> 条结果");
                    $list.html(html.join(''));
                    var html1 = [],html2=[],html3=[];
                    for(i = 0;i<res.statisticsIpc.length;i++)
                    {
                        html1.push(["<li ","class='stat'>",res.statisticsIpc[i][0]," : ",res.statisticsIpc[i][1],"</li>"].join(''));
                        console.log(res.statisticsIpc[i]);
                    }
                    for(i = 0;i<res.statisticsApplicant.length;i++)
                    {
                        html2.push("<li "+"class='stat'>"+res.statisticsApplicant[i][0]+" : "+res.statisticsApplicant[i][1]+"</li>");
                    }
                    for(i = 0;i<res.statisticsAgency.length;i++)
                    {
                        html3.push("<li "+"class='stat'>"+res.statisticsAgency[i][0]+" : "+res.statisticsAgency[i][1]+"</li>");
                    }
                    $postipc.html(html1.join(""));
                    $postapplicant.html(html2.join(""));
                    $postagency.html(html3.join(""));
                    console.log(html1);
                    markKeyWord(res.zh);
                }else if(res.code == 404) {
                    var html = [];
                    $('.page-wrapper').css("display",'none');
                    $('.info_404').css("display",'block');
                    html.push(html_404());
                    $('.info_404').html(html.join(''));
                }
            })
            .always(function(){
                pageView.enable();
            });
        }
            else if(flag==1){
           Ajax.get('/searchipc', data)
            .done(function (res) {
                if (res.code == 200) {
                    var total1 = res.total1;
                    var total = res.total;
                    pageView.refresh(total1);
                    var html = [],
                        renderItems = res.textList,
                        num = pageView.pageSize,
                        start = 1,
                        end = num,
                        flag = false;
                    for(var i = start-1; i < end ; i++) {
                        html.push(getItemHtml(renderItems[i], i, ipc));
                    }
                    $result.html("共搜索到 <span style='color:red;'>" + res.total + "</span> 条结果");
                    $list.html(html.join(''));
                    var html1 = [],html2=[],html3=[];
                    for(i = 0;i<res.statisticsIpc.length;i++)
                    {
                        html1.push("<li "+"class='stat'>"+res.statisticsIpc[i][0]+" : "+res.statisticsIpc[i][1]+"</li>");
                        console.log(res.statisticsIpc[i]);
                    }
                    for(i = 0;i<res.statisticsApplicant.length;i++)
                    {
                        html2.push("<li "+"class='stat'>"+res.statisticsApplicant[i][0]+" : "+res.statisticsApplicant[i][1]+"</li>");
                    }
                    for(i = 0;i<res.statisticsAgency.length;i++)
                    {
                        html3.push("<li "+"class='stat'>"+res.statisticsAgency[i][0]+" : "+res.statisticsAgency[i][1]+"</li>");
                    }
                    $postipc.html(html1.join(""));
                    $postapplicant.html(html2.join(""));
                    $postagency.html(html3.join(""));
                    console.log(html1);
                    markKeyWord(ipc);
                }else if(res.code == 404) {
                    var html = [];
                    $('.page-wrapper').css("display",'none');
                    $('.info_404').css("display",'block');
                    html.push(html_404());
                    $('.info_404').html(html.join(''));
                }
            })
            .always(function(){
                pageView.enable();
            });}
            else if(flag==2)
            {
                Ajax.get('/searchappnum', data)
            .done(function (res) {
                if (res.code == 200) {
                    var total1 = res.total1;
                    var total = res.total;
                    pageView.refresh(total1);
                    var html = [],
                        renderItems = res.textList,
                        num = pageView.pageSize,
                        start = pageView.data.start,
                        end = pageView.data.end,
                        flag = false;
                    for(var i = start-1; i < end ; i++) {
                        html.push(getItemHtml(renderItems[i], i, ipc));
                    }
                    $result.html("共搜索到 <span style='color:red;'>" + res.total + "</span> 条结果");
                    $list.html(html.join(''));
                    var html1 = [],html2=[],html3=[];
                    for(i = 0;i<res.statisticsIpc.length;i++)
                    {
                        html1.push("<li "+"class='stat'>"+res.statisticsIpc[i][0]+" : "+res.statisticsIpc[i][1]+"</li>");
                        console.log(res.statisticsIpc[i]);
                    }
                    for(i = 0;i<res.statisticsApplicant.length;i++)
                    {
                        html2.push("<li "+"class='stat'>"+res.statisticsApplicant[i][0]+" : "+res.statisticsApplicant[i][1]+"</li>");
                    }
                    for(i = 0;i<res.statisticsAgency.length;i++)
                    {
                        html3.push("<li "+"class='stat'>"+res.statisticsAgency[i][0]+" : "+res.statisticsAgency[i][1]+"</li>");
                    }
                    $postipc.html(html1.join(""));
                    $postapplicant.html(html2.join(""));
                    $postagency.html(html3.join(""));
                    console.log(html1);
                }else if(res.code == 404) {
                    var html = [];
                    $('.page-wrapper').css("display",'none');
                    $('.info_404').css("display",'block');
                    html.push(html_404());
                    $('.info_404').html(html.join(''));
                }
            })
            .always(function(){
                pageView.enable();
            });}
            else if(flag == 3){
                Ajax.get('/searchenzh', data)
            .done(function (res) {
                if (res.code == 200) {
                    console.log(res);
                    var total1 = res.total1;
                    var total = res.total;

                    pageView.refresh(total1);
                    var html = [],
                        renderItems = res.textList,
                        num = pageView.pageSize,
                        start = 1,
                        end = num,
                        flag = false;
                    for(var i = start-1; i < end ; i++) {
                        html.push(getItemHtml(renderItems[i], i, en));
                    }
                    $result.html("共搜索到 <span style='color:red;'>" + res.total + "</span> 条结果");
                    $list.html(html.join(''));
                    var html1 = [],html2=[],html3=[];
                    for(i = 0;i<res.statisticsIpc.length;i++)
                    {
                        html1.push(["<li ","class='stat'>",res.statisticsIpc[i][0]," : ",res.statisticsIpc[i][1],"</li>"].join(''));
                        console.log(res.statisticsIpc[i]);
                    }
                    for(i = 0;i<res.statisticsApplicant.length;i++)
                    {
                        html2.push("<li "+"class='stat'>"+res.statisticsApplicant[i][0]+" : "+res.statisticsApplicant[i][1]+"</li>");
                    }
                    for(i = 0;i<res.statisticsAgency.length;i++)
                    {
                        html3.push("<li "+"class='stat'>"+res.statisticsAgency[i][0]+" : "+res.statisticsAgency[i][1]+"</li>");
                    }
                    $postipc.html(html1.join(""));
                    $postapplicant.html(html2.join(""));
                    $postagency.html(html3.join(""));
                    console.log(html1);
                    markKeyWord(res.zh);
                }else if(res.code == 404) {
                    var html = [];
                    $('.page-wrapper').css("display",'none');
                    $('.info_404').css("display",'block');
                    html.push(html_404());
                    $('.info_404').html(html.join(''));
                }
            })
            .always(function(){
                pageView.enable();
            });

        }
            }

    // 寻找整篇文章中包含关键字的文本
    findKeyText = function(item, i, key) {
        var textContent = $('#textContent-' + i),
            text = item.replace('\r\n', ''),
            reg = new RegExp(key, 'g');

        return text.substr(0,200);
    }

    // 搜索关键字高亮
    markKeyWord = function(key) {
        var keys = key.split(' ');
        console.log(keys.length);
        for(i = 0;i<keys.length;i++)
        {   var content = $list.html();
            var values = content.split(keys[i]);
            console.log(keys[i]);
            $list.html(values.join('<span style="color:red;">' + keys[i] + '</span>'));
        }
    }
        $postipc = $('#1'),
        $postapplicant = $('#2');
        $postagency = $('#3');
        $list = $('#list'),
        $result = $('#result'),
        $title = $('#title'),
        pageView = new PageView('#page-view', {
            defaultSize: 20,
            onChange: getData
        });



    getData();
});