



<!DOCTYPE html>
<html>
<head>
 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" >
 <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" >
 
 <meta name="ROBOTS" content="NOARCHIVE">
 
 <link rel="icon" type="image/vnd.microsoft.icon" href="http://www.gstatic.com/codesite/ph/images/phosting.ico">
 
 
 <script type="text/javascript">
 
 
 
 
 var codesite_token = "ABZ6GAeQ5SSRchth9mbxnKeigZ0COlBM5Q:1432077715372";
 
 
 var CS_env = {"assetVersionPath": "http://www.gstatic.com/codesite/ph/3197964839662303775", "profileUrl": "/u/jmjacquet@gmail.com/", "projectHomeUrl": "/p/django-dynamic-formset", "token": "ABZ6GAeQ5SSRchth9mbxnKeigZ0COlBM5Q:1432077715372", "relativeBaseUrl": "", "domainName": null, "assetHostPath": "http://www.gstatic.com/codesite/ph", "projectName": "django-dynamic-formset", "loggedInUserEmail": "jmjacquet@gmail.com"};
 var _gaq = _gaq || [];
 _gaq.push(
 ['siteTracker._setAccount', 'UA-18071-1'],
 ['siteTracker._trackPageview']);
 
 _gaq.push(
 ['projectTracker._setAccount', 'UA-2402974-7'],
 ['projectTracker._trackPageview']);
 
 (function() {
 var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
 ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
 (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(ga);
 })();
 
 </script>
 
 
 <title>jquery.formset.js - 
 django-dynamic-formset -
 
 
 A jQuery plugin that allows you dynamically add new forms to a rendered django formset - Google Project Hosting
 </title>
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/3197964839662303775/css/core.css">
 
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/3197964839662303775/css/ph_detail.css" >
 
 
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/3197964839662303775/css/d_sb.css" >
 
 
 
<!--[if IE]>
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/3197964839662303775/css/d_ie.css" >
<![endif]-->
 <style type="text/css">
 .menuIcon.off { background: no-repeat url(http://www.gstatic.com/codesite/ph/images/dropdown_sprite.gif) 0 -42px }
 .menuIcon.on { background: no-repeat url(http://www.gstatic.com/codesite/ph/images/dropdown_sprite.gif) 0 -28px }
 .menuIcon.down { background: no-repeat url(http://www.gstatic.com/codesite/ph/images/dropdown_sprite.gif) 0 0; }
 
 
 
  tr.inline_comment {
 background: #fff;
 vertical-align: top;
 }
 div.draft, div.published {
 padding: .3em;
 border: 1px solid #999; 
 margin-bottom: .1em;
 font-family: arial, sans-serif;
 max-width: 60em;
 }
 div.draft {
 background: #ffa;
 } 
 div.published {
 background: #e5ecf9;
 }
 div.published .body, div.draft .body {
 padding: .5em .1em .1em .1em;
 max-width: 60em;
 white-space: pre-wrap;
 white-space: -moz-pre-wrap;
 white-space: -pre-wrap;
 white-space: -o-pre-wrap;
 word-wrap: break-word;
 font-size: 1em;
 }
 div.draft .actions {
 margin-left: 1em;
 font-size: 90%;
 }
 div.draft form {
 padding: .5em .5em .5em 0;
 }
 div.draft textarea, div.published textarea {
 width: 95%;
 height: 10em;
 font-family: arial, sans-serif;
 margin-bottom: .5em;
 }

 
 .nocursor, .nocursor td, .cursor_hidden, .cursor_hidden td {
 background-color: white;
 height: 2px;
 }
 .cursor, .cursor td {
 background-color: darkblue;
 height: 2px;
 display: '';
 }
 
 
.list {
 border: 1px solid white;
 border-bottom: 0;
}

 
 </style>
</head>
<body class="t4">
<script type="text/javascript">
 window.___gcfg = {lang: 'en'};
 (function() 
 {var po = document.createElement("script");
 po.type = "text/javascript"; po.async = true;po.src = "https://apis.google.com/js/plusone.js";
 var s = document.getElementsByTagName("script")[0];
 s.parentNode.insertBefore(po, s);
 })();
</script>
<div class="headbg">

 <div id="gaia">
 

 <span>
 
 
 
 <a href="#" id="multilogin-dropdown" onclick="return false;"
 ><u><b>jmjacquet@gmail.com</b></u> <small>&#9660;</small></a>
 
 
 | <a href="/u/jmjacquet@gmail.com/" id="projects-dropdown" onclick="return false;"
 ><u>My favorites</u> <small>&#9660;</small></a>
 | <a href="/u/jmjacquet@gmail.com/" onclick="_CS_click('/gb/ph/profile');"
 title="Profile, Updates, and Settings"
 ><u>Profile</u></a>
 | <a href="https://www.google.com/accounts/Logout?continue=http%3A%2F%2Fcode.google.com%2Fp%2Fdjango-dynamic-formset%2Fsource%2Fbrowse%2Ftrunk%2Fsrc%2Fjquery.formset.js" 
 onclick="_CS_click('/gb/ph/signout');"
 ><u>Sign out</u></a>
 
 </span>

 </div>

 <div class="gbh" style="left: 0pt;"></div>
 <div class="gbh" style="right: 0pt;"></div>
 
 
 <div style="height: 1px"></div>
<!--[if lte IE 7]>
<div style="text-align:center;">
Your version of Internet Explorer is not supported. Try a browser that
contributes to open source, such as <a href="http://www.firefox.com">Firefox</a>,
<a href="http://www.google.com/chrome">Google Chrome</a>, or
<a href="http://code.google.com/chrome/chromeframe/">Google Chrome Frame</a>.
</div>
<![endif]-->



 <table style="padding:0px; margin: 0px 0px 10px 0px; width:100%" cellpadding="0" cellspacing="0"
 itemscope itemtype="http://schema.org/CreativeWork">
 <tr style="height: 58px;">
 
 
 
 <td id="plogo">
 <link itemprop="url" href="/p/django-dynamic-formset">
 <a href="/p/django-dynamic-formset/">
 
 <img src="http://www.gstatic.com/codesite/ph/images/defaultlogo.png" alt="Logo" itemprop="image">
 
 </a>
 </td>
 
 <td style="padding-left: 0.5em">
 
 <div id="pname">
 <a href="/p/django-dynamic-formset/"><span itemprop="name">django-dynamic-formset</span></a>
 </div>
 
 <div id="psum">
 <a id="project_summary_link"
 href="/p/django-dynamic-formset/"><span itemprop="description">A jQuery plugin that allows you dynamically add new forms to a rendered django formset</span></a>
 
 </div>
 
 
 </td>
 <td style="white-space:nowrap;text-align:right; vertical-align:bottom;">
 
 <form action="/hosting/search">
 <input size="30" name="q" value="" type="text">
 
 <input type="submit" name="projectsearch" value="Search projects" >
 </form>
 
 </tr>
 </table>

</div>

 
<div id="mt" class="gtb"> 
 <a href="/p/django-dynamic-formset/" class="tab ">Project&nbsp;Home</a>
 
 
 
 
 <a href="/p/django-dynamic-formset/downloads/list" class="tab ">Downloads</a>
 
 
 
 
 
 <a href="/p/django-dynamic-formset/w/list" class="tab ">Wiki</a>
 
 
 
 
 
 <a href="/p/django-dynamic-formset/issues/list"
 class="tab ">Issues</a>
 
 
 
 
 
 <a href="/p/django-dynamic-formset/source/checkout"
 class="tab active">Source</a>
 
 
 
 
 
 
 
 
 <a href="https://code.google.com/export-to-github/export?project=django-dynamic-formset">
 <button>Export to GitHub</button>
 
 </a>
 
 
 
 
 
 <div class=gtbc></div>
</div>
<table cellspacing="0" cellpadding="0" width="100%" align="center" border="0" class="st">
 <tr>
 
 
 
 
 
 
 <td class="subt">
 <div class="st2">
 <div class="isf">
 
 


 <span class="inst1"><a href="/p/django-dynamic-formset/source/checkout">Checkout</a></span> &nbsp;
 <span class="inst2"><a href="/p/django-dynamic-formset/source/browse/">Browse</a></span> &nbsp;
 <span class="inst3"><a href="/p/django-dynamic-formset/source/list">Changes</a></span> &nbsp;
 
 
 
 
 
 
 
 </form>
 <script type="text/javascript">
 
 function codesearchQuery(form) {
 var query = document.getElementById('q').value;
 if (query) { form.action += '%20' + query; }
 }
 </script>
 </div>
</div>

 </td>
 
 
 
 <td align="right" valign="top" class="bevel-right"></td>
 </tr>
</table>


<script type="text/javascript">
 var cancelBubble = false;
 function _go(url) { document.location = url; }
</script>
<div id="maincol"
 
>

 




<div class="expand">
<div id="colcontrol">
<style type="text/css">
 #file_flipper { white-space: nowrap; padding-right: 2em; }
 #file_flipper.hidden { display: none; }
 #file_flipper .pagelink { color: #0000CC; text-decoration: underline; }
 #file_flipper #visiblefiles { padding-left: 0.5em; padding-right: 0.5em; }
</style>
<table id="nav_and_rev" class="list"
 cellpadding="0" cellspacing="0" width="100%">
 <tr>
 
 <td nowrap="nowrap" class="src_crumbs src_nav" width="33%">
 <strong class="src_nav">Source path:&nbsp;</strong>
 <span id="crumb_root">
 
 <a href="/p/django-dynamic-formset/source/browse/">svn</a>/&nbsp;</span>
 <span id="crumb_links" class="ifClosed"><a href="/p/django-dynamic-formset/source/browse/trunk/">trunk</a><span class="sp">/&nbsp;</span><a href="/p/django-dynamic-formset/source/browse/trunk/src/">src</a><span class="sp">/&nbsp;</span>jquery.formset.js</span>
 
 


 </td>
 
 
 <td nowrap="nowrap" width="33%" align="center">
 <a href="/p/django-dynamic-formset/source/browse/trunk/src/jquery.formset.js?edit=1"
 ><img src="http://www.gstatic.com/codesite/ph/images/pencil-y14.png"
 class="edit_icon">Edit file</a>
 </td>
 
 
 <td nowrap="nowrap" width="33%" align="right">
 <table cellpadding="0" cellspacing="0" style="font-size: 100%"><tr>
 
 
 <td class="flipper">
 <ul class="leftside">
 
 <li><a href="/p/django-dynamic-formset/source/browse/trunk/src/jquery.formset.js?r=15" title="Previous">&lsaquo;r15</a></li>
 
 </ul>
 </td>
 
 <td class="flipper"><b>r22</b></td>
 
 </tr></table>
 </td> 
 </tr>
</table>

<div class="fc">
 
 
 
<style type="text/css">
.undermouse span {
 background-image: url(http://www.gstatic.com/codesite/ph/images/comments.gif); }
</style>
<table class="opened" id="review_comment_area"
onmouseout="gutterOut()"><tr>
<td id="nums">
<pre><table width="100%"><tr class="nocursor"><td></td></tr></table></pre>
<pre><table width="100%" id="nums_table_0"><tr id="gr_svn22_1"

 onmouseover="gutterOver(1)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',1);">&nbsp;</span
></td><td id="1"><a href="#1">1</a></td></tr
><tr id="gr_svn22_2"

 onmouseover="gutterOver(2)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',2);">&nbsp;</span
></td><td id="2"><a href="#2">2</a></td></tr
><tr id="gr_svn22_3"

 onmouseover="gutterOver(3)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',3);">&nbsp;</span
></td><td id="3"><a href="#3">3</a></td></tr
><tr id="gr_svn22_4"

 onmouseover="gutterOver(4)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',4);">&nbsp;</span
></td><td id="4"><a href="#4">4</a></td></tr
><tr id="gr_svn22_5"

 onmouseover="gutterOver(5)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',5);">&nbsp;</span
></td><td id="5"><a href="#5">5</a></td></tr
><tr id="gr_svn22_6"

 onmouseover="gutterOver(6)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',6);">&nbsp;</span
></td><td id="6"><a href="#6">6</a></td></tr
><tr id="gr_svn22_7"

 onmouseover="gutterOver(7)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',7);">&nbsp;</span
></td><td id="7"><a href="#7">7</a></td></tr
><tr id="gr_svn22_8"

 onmouseover="gutterOver(8)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',8);">&nbsp;</span
></td><td id="8"><a href="#8">8</a></td></tr
><tr id="gr_svn22_9"

 onmouseover="gutterOver(9)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',9);">&nbsp;</span
></td><td id="9"><a href="#9">9</a></td></tr
><tr id="gr_svn22_10"

 onmouseover="gutterOver(10)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',10);">&nbsp;</span
></td><td id="10"><a href="#10">10</a></td></tr
><tr id="gr_svn22_11"

 onmouseover="gutterOver(11)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',11);">&nbsp;</span
></td><td id="11"><a href="#11">11</a></td></tr
><tr id="gr_svn22_12"

 onmouseover="gutterOver(12)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',12);">&nbsp;</span
></td><td id="12"><a href="#12">12</a></td></tr
><tr id="gr_svn22_13"

 onmouseover="gutterOver(13)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',13);">&nbsp;</span
></td><td id="13"><a href="#13">13</a></td></tr
><tr id="gr_svn22_14"

 onmouseover="gutterOver(14)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',14);">&nbsp;</span
></td><td id="14"><a href="#14">14</a></td></tr
><tr id="gr_svn22_15"

 onmouseover="gutterOver(15)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',15);">&nbsp;</span
></td><td id="15"><a href="#15">15</a></td></tr
><tr id="gr_svn22_16"

 onmouseover="gutterOver(16)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',16);">&nbsp;</span
></td><td id="16"><a href="#16">16</a></td></tr
><tr id="gr_svn22_17"

 onmouseover="gutterOver(17)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',17);">&nbsp;</span
></td><td id="17"><a href="#17">17</a></td></tr
><tr id="gr_svn22_18"

 onmouseover="gutterOver(18)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',18);">&nbsp;</span
></td><td id="18"><a href="#18">18</a></td></tr
><tr id="gr_svn22_19"

 onmouseover="gutterOver(19)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',19);">&nbsp;</span
></td><td id="19"><a href="#19">19</a></td></tr
><tr id="gr_svn22_20"

 onmouseover="gutterOver(20)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',20);">&nbsp;</span
></td><td id="20"><a href="#20">20</a></td></tr
><tr id="gr_svn22_21"

 onmouseover="gutterOver(21)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',21);">&nbsp;</span
></td><td id="21"><a href="#21">21</a></td></tr
><tr id="gr_svn22_22"

 onmouseover="gutterOver(22)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',22);">&nbsp;</span
></td><td id="22"><a href="#22">22</a></td></tr
><tr id="gr_svn22_23"

 onmouseover="gutterOver(23)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',23);">&nbsp;</span
></td><td id="23"><a href="#23">23</a></td></tr
><tr id="gr_svn22_24"

 onmouseover="gutterOver(24)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',24);">&nbsp;</span
></td><td id="24"><a href="#24">24</a></td></tr
><tr id="gr_svn22_25"

 onmouseover="gutterOver(25)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',25);">&nbsp;</span
></td><td id="25"><a href="#25">25</a></td></tr
><tr id="gr_svn22_26"

 onmouseover="gutterOver(26)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',26);">&nbsp;</span
></td><td id="26"><a href="#26">26</a></td></tr
><tr id="gr_svn22_27"

 onmouseover="gutterOver(27)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',27);">&nbsp;</span
></td><td id="27"><a href="#27">27</a></td></tr
><tr id="gr_svn22_28"

 onmouseover="gutterOver(28)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',28);">&nbsp;</span
></td><td id="28"><a href="#28">28</a></td></tr
><tr id="gr_svn22_29"

 onmouseover="gutterOver(29)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',29);">&nbsp;</span
></td><td id="29"><a href="#29">29</a></td></tr
><tr id="gr_svn22_30"

 onmouseover="gutterOver(30)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',30);">&nbsp;</span
></td><td id="30"><a href="#30">30</a></td></tr
><tr id="gr_svn22_31"

 onmouseover="gutterOver(31)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',31);">&nbsp;</span
></td><td id="31"><a href="#31">31</a></td></tr
><tr id="gr_svn22_32"

 onmouseover="gutterOver(32)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',32);">&nbsp;</span
></td><td id="32"><a href="#32">32</a></td></tr
><tr id="gr_svn22_33"

 onmouseover="gutterOver(33)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',33);">&nbsp;</span
></td><td id="33"><a href="#33">33</a></td></tr
><tr id="gr_svn22_34"

 onmouseover="gutterOver(34)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',34);">&nbsp;</span
></td><td id="34"><a href="#34">34</a></td></tr
><tr id="gr_svn22_35"

 onmouseover="gutterOver(35)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',35);">&nbsp;</span
></td><td id="35"><a href="#35">35</a></td></tr
><tr id="gr_svn22_36"

 onmouseover="gutterOver(36)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',36);">&nbsp;</span
></td><td id="36"><a href="#36">36</a></td></tr
><tr id="gr_svn22_37"

 onmouseover="gutterOver(37)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',37);">&nbsp;</span
></td><td id="37"><a href="#37">37</a></td></tr
><tr id="gr_svn22_38"

 onmouseover="gutterOver(38)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',38);">&nbsp;</span
></td><td id="38"><a href="#38">38</a></td></tr
><tr id="gr_svn22_39"

 onmouseover="gutterOver(39)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',39);">&nbsp;</span
></td><td id="39"><a href="#39">39</a></td></tr
><tr id="gr_svn22_40"

 onmouseover="gutterOver(40)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',40);">&nbsp;</span
></td><td id="40"><a href="#40">40</a></td></tr
><tr id="gr_svn22_41"

 onmouseover="gutterOver(41)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',41);">&nbsp;</span
></td><td id="41"><a href="#41">41</a></td></tr
><tr id="gr_svn22_42"

 onmouseover="gutterOver(42)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',42);">&nbsp;</span
></td><td id="42"><a href="#42">42</a></td></tr
><tr id="gr_svn22_43"

 onmouseover="gutterOver(43)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',43);">&nbsp;</span
></td><td id="43"><a href="#43">43</a></td></tr
><tr id="gr_svn22_44"

 onmouseover="gutterOver(44)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',44);">&nbsp;</span
></td><td id="44"><a href="#44">44</a></td></tr
><tr id="gr_svn22_45"

 onmouseover="gutterOver(45)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',45);">&nbsp;</span
></td><td id="45"><a href="#45">45</a></td></tr
><tr id="gr_svn22_46"

 onmouseover="gutterOver(46)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',46);">&nbsp;</span
></td><td id="46"><a href="#46">46</a></td></tr
><tr id="gr_svn22_47"

 onmouseover="gutterOver(47)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',47);">&nbsp;</span
></td><td id="47"><a href="#47">47</a></td></tr
><tr id="gr_svn22_48"

 onmouseover="gutterOver(48)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',48);">&nbsp;</span
></td><td id="48"><a href="#48">48</a></td></tr
><tr id="gr_svn22_49"

 onmouseover="gutterOver(49)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',49);">&nbsp;</span
></td><td id="49"><a href="#49">49</a></td></tr
><tr id="gr_svn22_50"

 onmouseover="gutterOver(50)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',50);">&nbsp;</span
></td><td id="50"><a href="#50">50</a></td></tr
><tr id="gr_svn22_51"

 onmouseover="gutterOver(51)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',51);">&nbsp;</span
></td><td id="51"><a href="#51">51</a></td></tr
><tr id="gr_svn22_52"

 onmouseover="gutterOver(52)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',52);">&nbsp;</span
></td><td id="52"><a href="#52">52</a></td></tr
><tr id="gr_svn22_53"

 onmouseover="gutterOver(53)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',53);">&nbsp;</span
></td><td id="53"><a href="#53">53</a></td></tr
><tr id="gr_svn22_54"

 onmouseover="gutterOver(54)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',54);">&nbsp;</span
></td><td id="54"><a href="#54">54</a></td></tr
><tr id="gr_svn22_55"

 onmouseover="gutterOver(55)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',55);">&nbsp;</span
></td><td id="55"><a href="#55">55</a></td></tr
><tr id="gr_svn22_56"

 onmouseover="gutterOver(56)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',56);">&nbsp;</span
></td><td id="56"><a href="#56">56</a></td></tr
><tr id="gr_svn22_57"

 onmouseover="gutterOver(57)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',57);">&nbsp;</span
></td><td id="57"><a href="#57">57</a></td></tr
><tr id="gr_svn22_58"

 onmouseover="gutterOver(58)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',58);">&nbsp;</span
></td><td id="58"><a href="#58">58</a></td></tr
><tr id="gr_svn22_59"

 onmouseover="gutterOver(59)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',59);">&nbsp;</span
></td><td id="59"><a href="#59">59</a></td></tr
><tr id="gr_svn22_60"

 onmouseover="gutterOver(60)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',60);">&nbsp;</span
></td><td id="60"><a href="#60">60</a></td></tr
><tr id="gr_svn22_61"

 onmouseover="gutterOver(61)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',61);">&nbsp;</span
></td><td id="61"><a href="#61">61</a></td></tr
><tr id="gr_svn22_62"

 onmouseover="gutterOver(62)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',62);">&nbsp;</span
></td><td id="62"><a href="#62">62</a></td></tr
><tr id="gr_svn22_63"

 onmouseover="gutterOver(63)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',63);">&nbsp;</span
></td><td id="63"><a href="#63">63</a></td></tr
><tr id="gr_svn22_64"

 onmouseover="gutterOver(64)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',64);">&nbsp;</span
></td><td id="64"><a href="#64">64</a></td></tr
><tr id="gr_svn22_65"

 onmouseover="gutterOver(65)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',65);">&nbsp;</span
></td><td id="65"><a href="#65">65</a></td></tr
><tr id="gr_svn22_66"

 onmouseover="gutterOver(66)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',66);">&nbsp;</span
></td><td id="66"><a href="#66">66</a></td></tr
><tr id="gr_svn22_67"

 onmouseover="gutterOver(67)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',67);">&nbsp;</span
></td><td id="67"><a href="#67">67</a></td></tr
><tr id="gr_svn22_68"

 onmouseover="gutterOver(68)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',68);">&nbsp;</span
></td><td id="68"><a href="#68">68</a></td></tr
><tr id="gr_svn22_69"

 onmouseover="gutterOver(69)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',69);">&nbsp;</span
></td><td id="69"><a href="#69">69</a></td></tr
><tr id="gr_svn22_70"

 onmouseover="gutterOver(70)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',70);">&nbsp;</span
></td><td id="70"><a href="#70">70</a></td></tr
><tr id="gr_svn22_71"

 onmouseover="gutterOver(71)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',71);">&nbsp;</span
></td><td id="71"><a href="#71">71</a></td></tr
><tr id="gr_svn22_72"

 onmouseover="gutterOver(72)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',72);">&nbsp;</span
></td><td id="72"><a href="#72">72</a></td></tr
><tr id="gr_svn22_73"

 onmouseover="gutterOver(73)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',73);">&nbsp;</span
></td><td id="73"><a href="#73">73</a></td></tr
><tr id="gr_svn22_74"

 onmouseover="gutterOver(74)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',74);">&nbsp;</span
></td><td id="74"><a href="#74">74</a></td></tr
><tr id="gr_svn22_75"

 onmouseover="gutterOver(75)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',75);">&nbsp;</span
></td><td id="75"><a href="#75">75</a></td></tr
><tr id="gr_svn22_76"

 onmouseover="gutterOver(76)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',76);">&nbsp;</span
></td><td id="76"><a href="#76">76</a></td></tr
><tr id="gr_svn22_77"

 onmouseover="gutterOver(77)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',77);">&nbsp;</span
></td><td id="77"><a href="#77">77</a></td></tr
><tr id="gr_svn22_78"

 onmouseover="gutterOver(78)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',78);">&nbsp;</span
></td><td id="78"><a href="#78">78</a></td></tr
><tr id="gr_svn22_79"

 onmouseover="gutterOver(79)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',79);">&nbsp;</span
></td><td id="79"><a href="#79">79</a></td></tr
><tr id="gr_svn22_80"

 onmouseover="gutterOver(80)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',80);">&nbsp;</span
></td><td id="80"><a href="#80">80</a></td></tr
><tr id="gr_svn22_81"

 onmouseover="gutterOver(81)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',81);">&nbsp;</span
></td><td id="81"><a href="#81">81</a></td></tr
><tr id="gr_svn22_82"

 onmouseover="gutterOver(82)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',82);">&nbsp;</span
></td><td id="82"><a href="#82">82</a></td></tr
><tr id="gr_svn22_83"

 onmouseover="gutterOver(83)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',83);">&nbsp;</span
></td><td id="83"><a href="#83">83</a></td></tr
><tr id="gr_svn22_84"

 onmouseover="gutterOver(84)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',84);">&nbsp;</span
></td><td id="84"><a href="#84">84</a></td></tr
><tr id="gr_svn22_85"

 onmouseover="gutterOver(85)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',85);">&nbsp;</span
></td><td id="85"><a href="#85">85</a></td></tr
><tr id="gr_svn22_86"

 onmouseover="gutterOver(86)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',86);">&nbsp;</span
></td><td id="86"><a href="#86">86</a></td></tr
><tr id="gr_svn22_87"

 onmouseover="gutterOver(87)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',87);">&nbsp;</span
></td><td id="87"><a href="#87">87</a></td></tr
><tr id="gr_svn22_88"

 onmouseover="gutterOver(88)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',88);">&nbsp;</span
></td><td id="88"><a href="#88">88</a></td></tr
><tr id="gr_svn22_89"

 onmouseover="gutterOver(89)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',89);">&nbsp;</span
></td><td id="89"><a href="#89">89</a></td></tr
><tr id="gr_svn22_90"

 onmouseover="gutterOver(90)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',90);">&nbsp;</span
></td><td id="90"><a href="#90">90</a></td></tr
><tr id="gr_svn22_91"

 onmouseover="gutterOver(91)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',91);">&nbsp;</span
></td><td id="91"><a href="#91">91</a></td></tr
><tr id="gr_svn22_92"

 onmouseover="gutterOver(92)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',92);">&nbsp;</span
></td><td id="92"><a href="#92">92</a></td></tr
><tr id="gr_svn22_93"

 onmouseover="gutterOver(93)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',93);">&nbsp;</span
></td><td id="93"><a href="#93">93</a></td></tr
><tr id="gr_svn22_94"

 onmouseover="gutterOver(94)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',94);">&nbsp;</span
></td><td id="94"><a href="#94">94</a></td></tr
><tr id="gr_svn22_95"

 onmouseover="gutterOver(95)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',95);">&nbsp;</span
></td><td id="95"><a href="#95">95</a></td></tr
><tr id="gr_svn22_96"

 onmouseover="gutterOver(96)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',96);">&nbsp;</span
></td><td id="96"><a href="#96">96</a></td></tr
><tr id="gr_svn22_97"

 onmouseover="gutterOver(97)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',97);">&nbsp;</span
></td><td id="97"><a href="#97">97</a></td></tr
><tr id="gr_svn22_98"

 onmouseover="gutterOver(98)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',98);">&nbsp;</span
></td><td id="98"><a href="#98">98</a></td></tr
><tr id="gr_svn22_99"

 onmouseover="gutterOver(99)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',99);">&nbsp;</span
></td><td id="99"><a href="#99">99</a></td></tr
><tr id="gr_svn22_100"

 onmouseover="gutterOver(100)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',100);">&nbsp;</span
></td><td id="100"><a href="#100">100</a></td></tr
><tr id="gr_svn22_101"

 onmouseover="gutterOver(101)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',101);">&nbsp;</span
></td><td id="101"><a href="#101">101</a></td></tr
><tr id="gr_svn22_102"

 onmouseover="gutterOver(102)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',102);">&nbsp;</span
></td><td id="102"><a href="#102">102</a></td></tr
><tr id="gr_svn22_103"

 onmouseover="gutterOver(103)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',103);">&nbsp;</span
></td><td id="103"><a href="#103">103</a></td></tr
><tr id="gr_svn22_104"

 onmouseover="gutterOver(104)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',104);">&nbsp;</span
></td><td id="104"><a href="#104">104</a></td></tr
><tr id="gr_svn22_105"

 onmouseover="gutterOver(105)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',105);">&nbsp;</span
></td><td id="105"><a href="#105">105</a></td></tr
><tr id="gr_svn22_106"

 onmouseover="gutterOver(106)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',106);">&nbsp;</span
></td><td id="106"><a href="#106">106</a></td></tr
><tr id="gr_svn22_107"

 onmouseover="gutterOver(107)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',107);">&nbsp;</span
></td><td id="107"><a href="#107">107</a></td></tr
><tr id="gr_svn22_108"

 onmouseover="gutterOver(108)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',108);">&nbsp;</span
></td><td id="108"><a href="#108">108</a></td></tr
><tr id="gr_svn22_109"

 onmouseover="gutterOver(109)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',109);">&nbsp;</span
></td><td id="109"><a href="#109">109</a></td></tr
><tr id="gr_svn22_110"

 onmouseover="gutterOver(110)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',110);">&nbsp;</span
></td><td id="110"><a href="#110">110</a></td></tr
><tr id="gr_svn22_111"

 onmouseover="gutterOver(111)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',111);">&nbsp;</span
></td><td id="111"><a href="#111">111</a></td></tr
><tr id="gr_svn22_112"

 onmouseover="gutterOver(112)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',112);">&nbsp;</span
></td><td id="112"><a href="#112">112</a></td></tr
><tr id="gr_svn22_113"

 onmouseover="gutterOver(113)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',113);">&nbsp;</span
></td><td id="113"><a href="#113">113</a></td></tr
><tr id="gr_svn22_114"

 onmouseover="gutterOver(114)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',114);">&nbsp;</span
></td><td id="114"><a href="#114">114</a></td></tr
><tr id="gr_svn22_115"

 onmouseover="gutterOver(115)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',115);">&nbsp;</span
></td><td id="115"><a href="#115">115</a></td></tr
><tr id="gr_svn22_116"

 onmouseover="gutterOver(116)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',116);">&nbsp;</span
></td><td id="116"><a href="#116">116</a></td></tr
><tr id="gr_svn22_117"

 onmouseover="gutterOver(117)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',117);">&nbsp;</span
></td><td id="117"><a href="#117">117</a></td></tr
><tr id="gr_svn22_118"

 onmouseover="gutterOver(118)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',118);">&nbsp;</span
></td><td id="118"><a href="#118">118</a></td></tr
><tr id="gr_svn22_119"

 onmouseover="gutterOver(119)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',119);">&nbsp;</span
></td><td id="119"><a href="#119">119</a></td></tr
><tr id="gr_svn22_120"

 onmouseover="gutterOver(120)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',120);">&nbsp;</span
></td><td id="120"><a href="#120">120</a></td></tr
><tr id="gr_svn22_121"

 onmouseover="gutterOver(121)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',121);">&nbsp;</span
></td><td id="121"><a href="#121">121</a></td></tr
><tr id="gr_svn22_122"

 onmouseover="gutterOver(122)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',122);">&nbsp;</span
></td><td id="122"><a href="#122">122</a></td></tr
><tr id="gr_svn22_123"

 onmouseover="gutterOver(123)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',123);">&nbsp;</span
></td><td id="123"><a href="#123">123</a></td></tr
><tr id="gr_svn22_124"

 onmouseover="gutterOver(124)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',124);">&nbsp;</span
></td><td id="124"><a href="#124">124</a></td></tr
><tr id="gr_svn22_125"

 onmouseover="gutterOver(125)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',125);">&nbsp;</span
></td><td id="125"><a href="#125">125</a></td></tr
><tr id="gr_svn22_126"

 onmouseover="gutterOver(126)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',126);">&nbsp;</span
></td><td id="126"><a href="#126">126</a></td></tr
><tr id="gr_svn22_127"

 onmouseover="gutterOver(127)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',127);">&nbsp;</span
></td><td id="127"><a href="#127">127</a></td></tr
><tr id="gr_svn22_128"

 onmouseover="gutterOver(128)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',128);">&nbsp;</span
></td><td id="128"><a href="#128">128</a></td></tr
><tr id="gr_svn22_129"

 onmouseover="gutterOver(129)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',129);">&nbsp;</span
></td><td id="129"><a href="#129">129</a></td></tr
><tr id="gr_svn22_130"

 onmouseover="gutterOver(130)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',130);">&nbsp;</span
></td><td id="130"><a href="#130">130</a></td></tr
><tr id="gr_svn22_131"

 onmouseover="gutterOver(131)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',131);">&nbsp;</span
></td><td id="131"><a href="#131">131</a></td></tr
><tr id="gr_svn22_132"

 onmouseover="gutterOver(132)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',132);">&nbsp;</span
></td><td id="132"><a href="#132">132</a></td></tr
><tr id="gr_svn22_133"

 onmouseover="gutterOver(133)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',133);">&nbsp;</span
></td><td id="133"><a href="#133">133</a></td></tr
><tr id="gr_svn22_134"

 onmouseover="gutterOver(134)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',134);">&nbsp;</span
></td><td id="134"><a href="#134">134</a></td></tr
><tr id="gr_svn22_135"

 onmouseover="gutterOver(135)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',135);">&nbsp;</span
></td><td id="135"><a href="#135">135</a></td></tr
><tr id="gr_svn22_136"

 onmouseover="gutterOver(136)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',136);">&nbsp;</span
></td><td id="136"><a href="#136">136</a></td></tr
><tr id="gr_svn22_137"

 onmouseover="gutterOver(137)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',137);">&nbsp;</span
></td><td id="137"><a href="#137">137</a></td></tr
><tr id="gr_svn22_138"

 onmouseover="gutterOver(138)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',138);">&nbsp;</span
></td><td id="138"><a href="#138">138</a></td></tr
><tr id="gr_svn22_139"

 onmouseover="gutterOver(139)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',139);">&nbsp;</span
></td><td id="139"><a href="#139">139</a></td></tr
><tr id="gr_svn22_140"

 onmouseover="gutterOver(140)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',140);">&nbsp;</span
></td><td id="140"><a href="#140">140</a></td></tr
><tr id="gr_svn22_141"

 onmouseover="gutterOver(141)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',141);">&nbsp;</span
></td><td id="141"><a href="#141">141</a></td></tr
><tr id="gr_svn22_142"

 onmouseover="gutterOver(142)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',142);">&nbsp;</span
></td><td id="142"><a href="#142">142</a></td></tr
><tr id="gr_svn22_143"

 onmouseover="gutterOver(143)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',143);">&nbsp;</span
></td><td id="143"><a href="#143">143</a></td></tr
><tr id="gr_svn22_144"

 onmouseover="gutterOver(144)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',144);">&nbsp;</span
></td><td id="144"><a href="#144">144</a></td></tr
><tr id="gr_svn22_145"

 onmouseover="gutterOver(145)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',145);">&nbsp;</span
></td><td id="145"><a href="#145">145</a></td></tr
><tr id="gr_svn22_146"

 onmouseover="gutterOver(146)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',146);">&nbsp;</span
></td><td id="146"><a href="#146">146</a></td></tr
><tr id="gr_svn22_147"

 onmouseover="gutterOver(147)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',147);">&nbsp;</span
></td><td id="147"><a href="#147">147</a></td></tr
><tr id="gr_svn22_148"

 onmouseover="gutterOver(148)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',148);">&nbsp;</span
></td><td id="148"><a href="#148">148</a></td></tr
><tr id="gr_svn22_149"

 onmouseover="gutterOver(149)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',149);">&nbsp;</span
></td><td id="149"><a href="#149">149</a></td></tr
><tr id="gr_svn22_150"

 onmouseover="gutterOver(150)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',150);">&nbsp;</span
></td><td id="150"><a href="#150">150</a></td></tr
><tr id="gr_svn22_151"

 onmouseover="gutterOver(151)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',151);">&nbsp;</span
></td><td id="151"><a href="#151">151</a></td></tr
><tr id="gr_svn22_152"

 onmouseover="gutterOver(152)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',152);">&nbsp;</span
></td><td id="152"><a href="#152">152</a></td></tr
><tr id="gr_svn22_153"

 onmouseover="gutterOver(153)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',153);">&nbsp;</span
></td><td id="153"><a href="#153">153</a></td></tr
><tr id="gr_svn22_154"

 onmouseover="gutterOver(154)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',154);">&nbsp;</span
></td><td id="154"><a href="#154">154</a></td></tr
><tr id="gr_svn22_155"

 onmouseover="gutterOver(155)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',155);">&nbsp;</span
></td><td id="155"><a href="#155">155</a></td></tr
><tr id="gr_svn22_156"

 onmouseover="gutterOver(156)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',156);">&nbsp;</span
></td><td id="156"><a href="#156">156</a></td></tr
><tr id="gr_svn22_157"

 onmouseover="gutterOver(157)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',157);">&nbsp;</span
></td><td id="157"><a href="#157">157</a></td></tr
><tr id="gr_svn22_158"

 onmouseover="gutterOver(158)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',158);">&nbsp;</span
></td><td id="158"><a href="#158">158</a></td></tr
><tr id="gr_svn22_159"

 onmouseover="gutterOver(159)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',159);">&nbsp;</span
></td><td id="159"><a href="#159">159</a></td></tr
><tr id="gr_svn22_160"

 onmouseover="gutterOver(160)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',160);">&nbsp;</span
></td><td id="160"><a href="#160">160</a></td></tr
><tr id="gr_svn22_161"

 onmouseover="gutterOver(161)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',161);">&nbsp;</span
></td><td id="161"><a href="#161">161</a></td></tr
><tr id="gr_svn22_162"

 onmouseover="gutterOver(162)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',162);">&nbsp;</span
></td><td id="162"><a href="#162">162</a></td></tr
><tr id="gr_svn22_163"

 onmouseover="gutterOver(163)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',163);">&nbsp;</span
></td><td id="163"><a href="#163">163</a></td></tr
><tr id="gr_svn22_164"

 onmouseover="gutterOver(164)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',164);">&nbsp;</span
></td><td id="164"><a href="#164">164</a></td></tr
><tr id="gr_svn22_165"

 onmouseover="gutterOver(165)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',165);">&nbsp;</span
></td><td id="165"><a href="#165">165</a></td></tr
><tr id="gr_svn22_166"

 onmouseover="gutterOver(166)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',166);">&nbsp;</span
></td><td id="166"><a href="#166">166</a></td></tr
><tr id="gr_svn22_167"

 onmouseover="gutterOver(167)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',167);">&nbsp;</span
></td><td id="167"><a href="#167">167</a></td></tr
><tr id="gr_svn22_168"

 onmouseover="gutterOver(168)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',168);">&nbsp;</span
></td><td id="168"><a href="#168">168</a></td></tr
><tr id="gr_svn22_169"

 onmouseover="gutterOver(169)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',169);">&nbsp;</span
></td><td id="169"><a href="#169">169</a></td></tr
><tr id="gr_svn22_170"

 onmouseover="gutterOver(170)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',170);">&nbsp;</span
></td><td id="170"><a href="#170">170</a></td></tr
><tr id="gr_svn22_171"

 onmouseover="gutterOver(171)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',171);">&nbsp;</span
></td><td id="171"><a href="#171">171</a></td></tr
><tr id="gr_svn22_172"

 onmouseover="gutterOver(172)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',172);">&nbsp;</span
></td><td id="172"><a href="#172">172</a></td></tr
><tr id="gr_svn22_173"

 onmouseover="gutterOver(173)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',173);">&nbsp;</span
></td><td id="173"><a href="#173">173</a></td></tr
><tr id="gr_svn22_174"

 onmouseover="gutterOver(174)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',174);">&nbsp;</span
></td><td id="174"><a href="#174">174</a></td></tr
><tr id="gr_svn22_175"

 onmouseover="gutterOver(175)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',175);">&nbsp;</span
></td><td id="175"><a href="#175">175</a></td></tr
><tr id="gr_svn22_176"

 onmouseover="gutterOver(176)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',176);">&nbsp;</span
></td><td id="176"><a href="#176">176</a></td></tr
><tr id="gr_svn22_177"

 onmouseover="gutterOver(177)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',177);">&nbsp;</span
></td><td id="177"><a href="#177">177</a></td></tr
><tr id="gr_svn22_178"

 onmouseover="gutterOver(178)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',178);">&nbsp;</span
></td><td id="178"><a href="#178">178</a></td></tr
><tr id="gr_svn22_179"

 onmouseover="gutterOver(179)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',179);">&nbsp;</span
></td><td id="179"><a href="#179">179</a></td></tr
><tr id="gr_svn22_180"

 onmouseover="gutterOver(180)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',180);">&nbsp;</span
></td><td id="180"><a href="#180">180</a></td></tr
><tr id="gr_svn22_181"

 onmouseover="gutterOver(181)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',181);">&nbsp;</span
></td><td id="181"><a href="#181">181</a></td></tr
><tr id="gr_svn22_182"

 onmouseover="gutterOver(182)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',182);">&nbsp;</span
></td><td id="182"><a href="#182">182</a></td></tr
><tr id="gr_svn22_183"

 onmouseover="gutterOver(183)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',183);">&nbsp;</span
></td><td id="183"><a href="#183">183</a></td></tr
><tr id="gr_svn22_184"

 onmouseover="gutterOver(184)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',184);">&nbsp;</span
></td><td id="184"><a href="#184">184</a></td></tr
><tr id="gr_svn22_185"

 onmouseover="gutterOver(185)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',185);">&nbsp;</span
></td><td id="185"><a href="#185">185</a></td></tr
><tr id="gr_svn22_186"

 onmouseover="gutterOver(186)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',186);">&nbsp;</span
></td><td id="186"><a href="#186">186</a></td></tr
><tr id="gr_svn22_187"

 onmouseover="gutterOver(187)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',187);">&nbsp;</span
></td><td id="187"><a href="#187">187</a></td></tr
><tr id="gr_svn22_188"

 onmouseover="gutterOver(188)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',188);">&nbsp;</span
></td><td id="188"><a href="#188">188</a></td></tr
><tr id="gr_svn22_189"

 onmouseover="gutterOver(189)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',189);">&nbsp;</span
></td><td id="189"><a href="#189">189</a></td></tr
><tr id="gr_svn22_190"

 onmouseover="gutterOver(190)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',190);">&nbsp;</span
></td><td id="190"><a href="#190">190</a></td></tr
><tr id="gr_svn22_191"

 onmouseover="gutterOver(191)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',191);">&nbsp;</span
></td><td id="191"><a href="#191">191</a></td></tr
><tr id="gr_svn22_192"

 onmouseover="gutterOver(192)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',192);">&nbsp;</span
></td><td id="192"><a href="#192">192</a></td></tr
><tr id="gr_svn22_193"

 onmouseover="gutterOver(193)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',193);">&nbsp;</span
></td><td id="193"><a href="#193">193</a></td></tr
><tr id="gr_svn22_194"

 onmouseover="gutterOver(194)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',194);">&nbsp;</span
></td><td id="194"><a href="#194">194</a></td></tr
><tr id="gr_svn22_195"

 onmouseover="gutterOver(195)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',195);">&nbsp;</span
></td><td id="195"><a href="#195">195</a></td></tr
><tr id="gr_svn22_196"

 onmouseover="gutterOver(196)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',196);">&nbsp;</span
></td><td id="196"><a href="#196">196</a></td></tr
><tr id="gr_svn22_197"

 onmouseover="gutterOver(197)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',197);">&nbsp;</span
></td><td id="197"><a href="#197">197</a></td></tr
><tr id="gr_svn22_198"

 onmouseover="gutterOver(198)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',198);">&nbsp;</span
></td><td id="198"><a href="#198">198</a></td></tr
><tr id="gr_svn22_199"

 onmouseover="gutterOver(199)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',199);">&nbsp;</span
></td><td id="199"><a href="#199">199</a></td></tr
><tr id="gr_svn22_200"

 onmouseover="gutterOver(200)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',200);">&nbsp;</span
></td><td id="200"><a href="#200">200</a></td></tr
><tr id="gr_svn22_201"

 onmouseover="gutterOver(201)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',201);">&nbsp;</span
></td><td id="201"><a href="#201">201</a></td></tr
><tr id="gr_svn22_202"

 onmouseover="gutterOver(202)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',202);">&nbsp;</span
></td><td id="202"><a href="#202">202</a></td></tr
><tr id="gr_svn22_203"

 onmouseover="gutterOver(203)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',203);">&nbsp;</span
></td><td id="203"><a href="#203">203</a></td></tr
><tr id="gr_svn22_204"

 onmouseover="gutterOver(204)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',204);">&nbsp;</span
></td><td id="204"><a href="#204">204</a></td></tr
><tr id="gr_svn22_205"

 onmouseover="gutterOver(205)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',205);">&nbsp;</span
></td><td id="205"><a href="#205">205</a></td></tr
><tr id="gr_svn22_206"

 onmouseover="gutterOver(206)"

><td><span title="Add comment" onclick="codereviews.startEdit('svn22',206);">&nbsp;</span
></td><td id="206"><a href="#206">206</a></td></tr
></table></pre>
<pre><table width="100%"><tr class="nocursor"><td></td></tr></table></pre>
</td>
<td id="lines">
<pre><table width="100%"><tr class="cursor_stop cursor_hidden"><td></td></tr></table></pre>
<pre class="prettyprint lang-js"><table id="src_table_0"><tr
id=sl_svn22_1

 onmouseover="gutterOver(1)"

><td class="source">/**<br></td></tr
><tr
id=sl_svn22_2

 onmouseover="gutterOver(2)"

><td class="source"> * jQuery Formset 1.3-pre<br></td></tr
><tr
id=sl_svn22_3

 onmouseover="gutterOver(3)"

><td class="source"> * @author Stanislaus Madueke (stan DOT madueke AT gmail DOT com)<br></td></tr
><tr
id=sl_svn22_4

 onmouseover="gutterOver(4)"

><td class="source"> * @requires jQuery 1.2.6 or later<br></td></tr
><tr
id=sl_svn22_5

 onmouseover="gutterOver(5)"

><td class="source"> *<br></td></tr
><tr
id=sl_svn22_6

 onmouseover="gutterOver(6)"

><td class="source"> * Copyright (c) 2009, Stanislaus Madueke<br></td></tr
><tr
id=sl_svn22_7

 onmouseover="gutterOver(7)"

><td class="source"> * All rights reserved.<br></td></tr
><tr
id=sl_svn22_8

 onmouseover="gutterOver(8)"

><td class="source"> *<br></td></tr
><tr
id=sl_svn22_9

 onmouseover="gutterOver(9)"

><td class="source"> * Licensed under the New BSD License<br></td></tr
><tr
id=sl_svn22_10

 onmouseover="gutterOver(10)"

><td class="source"> * See: http://www.opensource.org/licenses/bsd-license.php<br></td></tr
><tr
id=sl_svn22_11

 onmouseover="gutterOver(11)"

><td class="source"> */<br></td></tr
><tr
id=sl_svn22_12

 onmouseover="gutterOver(12)"

><td class="source">;(function($) {<br></td></tr
><tr
id=sl_svn22_13

 onmouseover="gutterOver(13)"

><td class="source">    $.fn.formset = function(opts)<br></td></tr
><tr
id=sl_svn22_14

 onmouseover="gutterOver(14)"

><td class="source">    {<br></td></tr
><tr
id=sl_svn22_15

 onmouseover="gutterOver(15)"

><td class="source">        var options = $.extend({}, $.fn.formset.defaults, opts),<br></td></tr
><tr
id=sl_svn22_16

 onmouseover="gutterOver(16)"

><td class="source">            flatExtraClasses = options.extraClasses.join(&#39; &#39;),<br></td></tr
><tr
id=sl_svn22_17

 onmouseover="gutterOver(17)"

><td class="source">            totalForms = $(&#39;#id_&#39; + options.prefix + &#39;-TOTAL_FORMS&#39;),<br></td></tr
><tr
id=sl_svn22_18

 onmouseover="gutterOver(18)"

><td class="source">            maxForms = $(&#39;#id_&#39; + options.prefix + &#39;-MAX_NUM_FORMS&#39;),<br></td></tr
><tr
id=sl_svn22_19

 onmouseover="gutterOver(19)"

><td class="source">            childElementSelector = &#39;input,select,textarea,label,div&#39;,<br></td></tr
><tr
id=sl_svn22_20

 onmouseover="gutterOver(20)"

><td class="source">            $$ = $(this),<br></td></tr
><tr
id=sl_svn22_21

 onmouseover="gutterOver(21)"

><td class="source"><br></td></tr
><tr
id=sl_svn22_22

 onmouseover="gutterOver(22)"

><td class="source">            applyExtraClasses = function(row, ndx) {<br></td></tr
><tr
id=sl_svn22_23

 onmouseover="gutterOver(23)"

><td class="source">                if (options.extraClasses) {<br></td></tr
><tr
id=sl_svn22_24

 onmouseover="gutterOver(24)"

><td class="source">                    row.removeClass(flatExtraClasses);<br></td></tr
><tr
id=sl_svn22_25

 onmouseover="gutterOver(25)"

><td class="source">                    row.addClass(options.extraClasses[ndx % options.extraClasses.length]);<br></td></tr
><tr
id=sl_svn22_26

 onmouseover="gutterOver(26)"

><td class="source">                }<br></td></tr
><tr
id=sl_svn22_27

 onmouseover="gutterOver(27)"

><td class="source">            },<br></td></tr
><tr
id=sl_svn22_28

 onmouseover="gutterOver(28)"

><td class="source"><br></td></tr
><tr
id=sl_svn22_29

 onmouseover="gutterOver(29)"

><td class="source">            updateElementIndex = function(elem, prefix, ndx) {<br></td></tr
><tr
id=sl_svn22_30

 onmouseover="gutterOver(30)"

><td class="source">                var idRegex = new RegExp(prefix + &#39;-(\\d+|__prefix__)-&#39;),<br></td></tr
><tr
id=sl_svn22_31

 onmouseover="gutterOver(31)"

><td class="source">                    replacement = prefix + &#39;-&#39; + ndx + &#39;-&#39;;<br></td></tr
><tr
id=sl_svn22_32

 onmouseover="gutterOver(32)"

><td class="source">                if (elem.attr(&quot;for&quot;)) elem.attr(&quot;for&quot;, elem.attr(&quot;for&quot;).replace(idRegex, replacement));<br></td></tr
><tr
id=sl_svn22_33

 onmouseover="gutterOver(33)"

><td class="source">                if (elem.attr(&#39;id&#39;)) elem.attr(&#39;id&#39;, elem.attr(&#39;id&#39;).replace(idRegex, replacement));<br></td></tr
><tr
id=sl_svn22_34

 onmouseover="gutterOver(34)"

><td class="source">                if (elem.attr(&#39;name&#39;)) elem.attr(&#39;name&#39;, elem.attr(&#39;name&#39;).replace(idRegex, replacement));<br></td></tr
><tr
id=sl_svn22_35

 onmouseover="gutterOver(35)"

><td class="source">            },<br></td></tr
><tr
id=sl_svn22_36

 onmouseover="gutterOver(36)"

><td class="source"><br></td></tr
><tr
id=sl_svn22_37

 onmouseover="gutterOver(37)"

><td class="source">            hasChildElements = function(row) {<br></td></tr
><tr
id=sl_svn22_38

 onmouseover="gutterOver(38)"

><td class="source">                return row.find(childElementSelector).length &gt; 0;<br></td></tr
><tr
id=sl_svn22_39

 onmouseover="gutterOver(39)"

><td class="source">            },<br></td></tr
><tr
id=sl_svn22_40

 onmouseover="gutterOver(40)"

><td class="source"><br></td></tr
><tr
id=sl_svn22_41

 onmouseover="gutterOver(41)"

><td class="source">            showAddButton = function() {<br></td></tr
><tr
id=sl_svn22_42

 onmouseover="gutterOver(42)"

><td class="source">                return maxForms.length == 0 ||   // For Django versions pre 1.2<br></td></tr
><tr
id=sl_svn22_43

 onmouseover="gutterOver(43)"

><td class="source">                    (maxForms.val() == &#39;&#39; || (maxForms.val() - totalForms.val() &gt; 0))<br></td></tr
><tr
id=sl_svn22_44

 onmouseover="gutterOver(44)"

><td class="source">            },<br></td></tr
><tr
id=sl_svn22_45

 onmouseover="gutterOver(45)"

><td class="source"><br></td></tr
><tr
id=sl_svn22_46

 onmouseover="gutterOver(46)"

><td class="source">            insertDeleteLink = function(row) {<br></td></tr
><tr
id=sl_svn22_47

 onmouseover="gutterOver(47)"

><td class="source">                if (row.is(&#39;TR&#39;)) {<br></td></tr
><tr
id=sl_svn22_48

 onmouseover="gutterOver(48)"

><td class="source">                    // If the forms are laid out in table rows, insert<br></td></tr
><tr
id=sl_svn22_49

 onmouseover="gutterOver(49)"

><td class="source">                    // the remove button into the last table cell:<br></td></tr
><tr
id=sl_svn22_50

 onmouseover="gutterOver(50)"

><td class="source">                    row.children(&#39;:last&#39;).append(&#39;&lt;a class=&quot;&#39; + options.deleteCssClass +&#39;&quot; href=&quot;javascript:void(0)&quot;&gt;&#39; + options.deleteText + &#39;&lt;/a&gt;&#39;);<br></td></tr
><tr
id=sl_svn22_51

 onmouseover="gutterOver(51)"

><td class="source">                } else if (row.is(&#39;UL&#39;) || row.is(&#39;OL&#39;)) {<br></td></tr
><tr
id=sl_svn22_52

 onmouseover="gutterOver(52)"

><td class="source">                    // If they&#39;re laid out as an ordered/unordered list,<br></td></tr
><tr
id=sl_svn22_53

 onmouseover="gutterOver(53)"

><td class="source">                    // insert an &lt;li&gt; after the last list item:<br></td></tr
><tr
id=sl_svn22_54

 onmouseover="gutterOver(54)"

><td class="source">                    row.append(&#39;&lt;li&gt;&lt;a class=&quot;&#39; + options.deleteCssClass + &#39;&quot; href=&quot;javascript:void(0)&quot;&gt;&#39; + options.deleteText +&#39;&lt;/a&gt;&lt;/li&gt;&#39;);<br></td></tr
><tr
id=sl_svn22_55

 onmouseover="gutterOver(55)"

><td class="source">                } else {<br></td></tr
><tr
id=sl_svn22_56

 onmouseover="gutterOver(56)"

><td class="source">                    // Otherwise, just insert the remove button as the<br></td></tr
><tr
id=sl_svn22_57

 onmouseover="gutterOver(57)"

><td class="source">                    // last child element of the form&#39;s container:<br></td></tr
><tr
id=sl_svn22_58

 onmouseover="gutterOver(58)"

><td class="source">                    row.append(&#39;&lt;a class=&quot;&#39; + options.deleteCssClass + &#39;&quot; href=&quot;javascript:void(0)&quot;&gt;&#39; + options.deleteText +&#39;&lt;/a&gt;&#39;);<br></td></tr
><tr
id=sl_svn22_59

 onmouseover="gutterOver(59)"

><td class="source">                }<br></td></tr
><tr
id=sl_svn22_60

 onmouseover="gutterOver(60)"

><td class="source">                row.find(&#39;a.&#39; + options.deleteCssClass).click(function() {<br></td></tr
><tr
id=sl_svn22_61

 onmouseover="gutterOver(61)"

><td class="source">                    var row = $(this).parents(&#39;.&#39; + options.formCssClass),<br></td></tr
><tr
id=sl_svn22_62

 onmouseover="gutterOver(62)"

><td class="source">                        del = row.find(&#39;input:hidden[id $= &quot;-DELETE&quot;]&#39;),<br></td></tr
><tr
id=sl_svn22_63

 onmouseover="gutterOver(63)"

><td class="source">                        buttonRow = row.siblings(&quot;a.&quot; + options.addCssClass + &#39;, .&#39; + options.formCssClass + &#39;-add&#39;),<br></td></tr
><tr
id=sl_svn22_64

 onmouseover="gutterOver(64)"

><td class="source">                        forms;<br></td></tr
><tr
id=sl_svn22_65

 onmouseover="gutterOver(65)"

><td class="source">                    if (del.length) {<br></td></tr
><tr
id=sl_svn22_66

 onmouseover="gutterOver(66)"

><td class="source">                        // We&#39;re dealing with an inline formset.<br></td></tr
><tr
id=sl_svn22_67

 onmouseover="gutterOver(67)"

><td class="source">                        // Rather than remove this form from the DOM, we&#39;ll mark it as deleted<br></td></tr
><tr
id=sl_svn22_68

 onmouseover="gutterOver(68)"

><td class="source">                        // and hide it, then let Django handle the deleting:<br></td></tr
><tr
id=sl_svn22_69

 onmouseover="gutterOver(69)"

><td class="source">                        del.val(&#39;on&#39;);<br></td></tr
><tr
id=sl_svn22_70

 onmouseover="gutterOver(70)"

><td class="source">                        row.hide();<br></td></tr
><tr
id=sl_svn22_71

 onmouseover="gutterOver(71)"

><td class="source">                        forms = $(&#39;.&#39; + options.formCssClass).not(&#39;:hidden&#39;);<br></td></tr
><tr
id=sl_svn22_72

 onmouseover="gutterOver(72)"

><td class="source">                    } else {<br></td></tr
><tr
id=sl_svn22_73

 onmouseover="gutterOver(73)"

><td class="source">                        row.remove();<br></td></tr
><tr
id=sl_svn22_74

 onmouseover="gutterOver(74)"

><td class="source">                        // Update the TOTAL_FORMS count:<br></td></tr
><tr
id=sl_svn22_75

 onmouseover="gutterOver(75)"

><td class="source">                        forms = $(&#39;.&#39; + options.formCssClass).not(&#39;.formset-custom-template&#39;);<br></td></tr
><tr
id=sl_svn22_76

 onmouseover="gutterOver(76)"

><td class="source">                        totalForms.val(forms.length);<br></td></tr
><tr
id=sl_svn22_77

 onmouseover="gutterOver(77)"

><td class="source">                    }<br></td></tr
><tr
id=sl_svn22_78

 onmouseover="gutterOver(78)"

><td class="source">                    for (var i=0, formCount=forms.length; i&lt;formCount; i++) {<br></td></tr
><tr
id=sl_svn22_79

 onmouseover="gutterOver(79)"

><td class="source">                        // Apply `extraClasses` to form rows so they&#39;re nicely alternating:<br></td></tr
><tr
id=sl_svn22_80

 onmouseover="gutterOver(80)"

><td class="source">                        applyExtraClasses(forms.eq(i), i);<br></td></tr
><tr
id=sl_svn22_81

 onmouseover="gutterOver(81)"

><td class="source">                        if (!del.length) {<br></td></tr
><tr
id=sl_svn22_82

 onmouseover="gutterOver(82)"

><td class="source">                            // Also update names and IDs for all child controls (if this isn&#39;t<br></td></tr
><tr
id=sl_svn22_83

 onmouseover="gutterOver(83)"

><td class="source">                            // a delete-able inline formset) so they remain in sequence:<br></td></tr
><tr
id=sl_svn22_84

 onmouseover="gutterOver(84)"

><td class="source">                            forms.eq(i).find(childElementSelector).each(function() {<br></td></tr
><tr
id=sl_svn22_85

 onmouseover="gutterOver(85)"

><td class="source">                                updateElementIndex($(this), options.prefix, i);<br></td></tr
><tr
id=sl_svn22_86

 onmouseover="gutterOver(86)"

><td class="source">                            });<br></td></tr
><tr
id=sl_svn22_87

 onmouseover="gutterOver(87)"

><td class="source">                        }<br></td></tr
><tr
id=sl_svn22_88

 onmouseover="gutterOver(88)"

><td class="source">                    }<br></td></tr
><tr
id=sl_svn22_89

 onmouseover="gutterOver(89)"

><td class="source">                    // Check if we need to show the add button:<br></td></tr
><tr
id=sl_svn22_90

 onmouseover="gutterOver(90)"

><td class="source">                    if (buttonRow.is(&#39;:hidden&#39;) &amp;&amp; showAddButton()) buttonRow.show();<br></td></tr
><tr
id=sl_svn22_91

 onmouseover="gutterOver(91)"

><td class="source">                    // If a post-delete callback was provided, call it with the deleted form:<br></td></tr
><tr
id=sl_svn22_92

 onmouseover="gutterOver(92)"

><td class="source">                    if (options.removed) options.removed(row);<br></td></tr
><tr
id=sl_svn22_93

 onmouseover="gutterOver(93)"

><td class="source">                    return false;<br></td></tr
><tr
id=sl_svn22_94

 onmouseover="gutterOver(94)"

><td class="source">                });<br></td></tr
><tr
id=sl_svn22_95

 onmouseover="gutterOver(95)"

><td class="source">            };<br></td></tr
><tr
id=sl_svn22_96

 onmouseover="gutterOver(96)"

><td class="source"><br></td></tr
><tr
id=sl_svn22_97

 onmouseover="gutterOver(97)"

><td class="source">        $$.each(function(i) {<br></td></tr
><tr
id=sl_svn22_98

 onmouseover="gutterOver(98)"

><td class="source">            var row = $(this),<br></td></tr
><tr
id=sl_svn22_99

 onmouseover="gutterOver(99)"

><td class="source">                del = row.find(&#39;input:checkbox[id $= &quot;-DELETE&quot;]&#39;);<br></td></tr
><tr
id=sl_svn22_100

 onmouseover="gutterOver(100)"

><td class="source">            if (del.length) {<br></td></tr
><tr
id=sl_svn22_101

 onmouseover="gutterOver(101)"

><td class="source">                // If you specify &quot;can_delete = True&quot; when creating an inline formset,<br></td></tr
><tr
id=sl_svn22_102

 onmouseover="gutterOver(102)"

><td class="source">                // Django adds a checkbox to each form in the formset.<br></td></tr
><tr
id=sl_svn22_103

 onmouseover="gutterOver(103)"

><td class="source">                // Replace the default checkbox with a hidden field:<br></td></tr
><tr
id=sl_svn22_104

 onmouseover="gutterOver(104)"

><td class="source">                if (del.is(&#39;:checked&#39;)) {<br></td></tr
><tr
id=sl_svn22_105

 onmouseover="gutterOver(105)"

><td class="source">                    // If an inline formset containing deleted forms fails validation, make sure<br></td></tr
><tr
id=sl_svn22_106

 onmouseover="gutterOver(106)"

><td class="source">                    // we keep the forms hidden (thanks for the bug report and suggested fix Mike)<br></td></tr
><tr
id=sl_svn22_107

 onmouseover="gutterOver(107)"

><td class="source">                    del.before(&#39;&lt;input type=&quot;hidden&quot; name=&quot;&#39; + del.attr(&#39;name&#39;) +&#39;&quot; id=&quot;&#39; + del.attr(&#39;id&#39;) +&#39;&quot; value=&quot;on&quot; /&gt;&#39;);<br></td></tr
><tr
id=sl_svn22_108

 onmouseover="gutterOver(108)"

><td class="source">                    row.hide();<br></td></tr
><tr
id=sl_svn22_109

 onmouseover="gutterOver(109)"

><td class="source">                } else {<br></td></tr
><tr
id=sl_svn22_110

 onmouseover="gutterOver(110)"

><td class="source">                    del.before(&#39;&lt;input type=&quot;hidden&quot; name=&quot;&#39; + del.attr(&#39;name&#39;) +&#39;&quot; id=&quot;&#39; + del.attr(&#39;id&#39;) +&#39;&quot; /&gt;&#39;);<br></td></tr
><tr
id=sl_svn22_111

 onmouseover="gutterOver(111)"

><td class="source">                }<br></td></tr
><tr
id=sl_svn22_112

 onmouseover="gutterOver(112)"

><td class="source">                // Hide any labels associated with the DELETE checkbox:<br></td></tr
><tr
id=sl_svn22_113

 onmouseover="gutterOver(113)"

><td class="source">                $(&#39;label[for=&quot;&#39; + del.attr(&#39;id&#39;) + &#39;&quot;]&#39;).hide();<br></td></tr
><tr
id=sl_svn22_114

 onmouseover="gutterOver(114)"

><td class="source">                del.remove();<br></td></tr
><tr
id=sl_svn22_115

 onmouseover="gutterOver(115)"

><td class="source">            }<br></td></tr
><tr
id=sl_svn22_116

 onmouseover="gutterOver(116)"

><td class="source">            if (hasChildElements(row)) {<br></td></tr
><tr
id=sl_svn22_117

 onmouseover="gutterOver(117)"

><td class="source">                row.addClass(options.formCssClass);<br></td></tr
><tr
id=sl_svn22_118

 onmouseover="gutterOver(118)"

><td class="source">                if (row.is(&#39;:visible&#39;)) {<br></td></tr
><tr
id=sl_svn22_119

 onmouseover="gutterOver(119)"

><td class="source">                    insertDeleteLink(row);<br></td></tr
><tr
id=sl_svn22_120

 onmouseover="gutterOver(120)"

><td class="source">                    applyExtraClasses(row, i);<br></td></tr
><tr
id=sl_svn22_121

 onmouseover="gutterOver(121)"

><td class="source">                }<br></td></tr
><tr
id=sl_svn22_122

 onmouseover="gutterOver(122)"

><td class="source">            }<br></td></tr
><tr
id=sl_svn22_123

 onmouseover="gutterOver(123)"

><td class="source">        });<br></td></tr
><tr
id=sl_svn22_124

 onmouseover="gutterOver(124)"

><td class="source"><br></td></tr
><tr
id=sl_svn22_125

 onmouseover="gutterOver(125)"

><td class="source">        if ($$.length) {<br></td></tr
><tr
id=sl_svn22_126

 onmouseover="gutterOver(126)"

><td class="source">            var hideAddButton = !showAddButton(),<br></td></tr
><tr
id=sl_svn22_127

 onmouseover="gutterOver(127)"

><td class="source">                addButton, template;<br></td></tr
><tr
id=sl_svn22_128

 onmouseover="gutterOver(128)"

><td class="source">            if (options.formTemplate) {<br></td></tr
><tr
id=sl_svn22_129

 onmouseover="gutterOver(129)"

><td class="source">                // If a form template was specified, we&#39;ll clone it to generate new form instances:<br></td></tr
><tr
id=sl_svn22_130

 onmouseover="gutterOver(130)"

><td class="source">                template = (options.formTemplate instanceof $) ? options.formTemplate : $(options.formTemplate);<br></td></tr
><tr
id=sl_svn22_131

 onmouseover="gutterOver(131)"

><td class="source">                template.removeAttr(&#39;id&#39;).addClass(options.formCssClass + &#39; formset-custom-template&#39;);<br></td></tr
><tr
id=sl_svn22_132

 onmouseover="gutterOver(132)"

><td class="source">                template.find(childElementSelector).each(function() {<br></td></tr
><tr
id=sl_svn22_133

 onmouseover="gutterOver(133)"

><td class="source">                    updateElementIndex($(this), options.prefix, &#39;__prefix__&#39;);<br></td></tr
><tr
id=sl_svn22_134

 onmouseover="gutterOver(134)"

><td class="source">                });<br></td></tr
><tr
id=sl_svn22_135

 onmouseover="gutterOver(135)"

><td class="source">                insertDeleteLink(template);<br></td></tr
><tr
id=sl_svn22_136

 onmouseover="gutterOver(136)"

><td class="source">            } else {<br></td></tr
><tr
id=sl_svn22_137

 onmouseover="gutterOver(137)"

><td class="source">                // Otherwise, use the last form in the formset; this works much better if you&#39;ve got<br></td></tr
><tr
id=sl_svn22_138

 onmouseover="gutterOver(138)"

><td class="source">                // extra (&gt;= 1) forms (thnaks to justhamade for pointing this out):<br></td></tr
><tr
id=sl_svn22_139

 onmouseover="gutterOver(139)"

><td class="source">                template = $(&#39;.&#39; + options.formCssClass + &#39;:last&#39;).clone(true).removeAttr(&#39;id&#39;);<br></td></tr
><tr
id=sl_svn22_140

 onmouseover="gutterOver(140)"

><td class="source">                template.find(&#39;input:hidden[id $= &quot;-DELETE&quot;]&#39;).remove();<br></td></tr
><tr
id=sl_svn22_141

 onmouseover="gutterOver(141)"

><td class="source">                // Clear all cloned fields, except those the user wants to keep (thanks to brunogola for the suggestion):<br></td></tr
><tr
id=sl_svn22_142

 onmouseover="gutterOver(142)"

><td class="source">                template.find(childElementSelector).not(options.keepFieldValues).each(function() {<br></td></tr
><tr
id=sl_svn22_143

 onmouseover="gutterOver(143)"

><td class="source">                    var elem = $(this);<br></td></tr
><tr
id=sl_svn22_144

 onmouseover="gutterOver(144)"

><td class="source">                    // If this is a checkbox or radiobutton, uncheck it.<br></td></tr
><tr
id=sl_svn22_145

 onmouseover="gutterOver(145)"

><td class="source">                    // This fixes Issue 1, reported by Wilson.Andrew.J:<br></td></tr
><tr
id=sl_svn22_146

 onmouseover="gutterOver(146)"

><td class="source">                    if (elem.is(&#39;input:checkbox&#39;) || elem.is(&#39;input:radio&#39;)) {<br></td></tr
><tr
id=sl_svn22_147

 onmouseover="gutterOver(147)"

><td class="source">                        elem.attr(&#39;checked&#39;, false);<br></td></tr
><tr
id=sl_svn22_148

 onmouseover="gutterOver(148)"

><td class="source">                    } else {<br></td></tr
><tr
id=sl_svn22_149

 onmouseover="gutterOver(149)"

><td class="source">                        elem.val(&#39;&#39;);<br></td></tr
><tr
id=sl_svn22_150

 onmouseover="gutterOver(150)"

><td class="source">                    }<br></td></tr
><tr
id=sl_svn22_151

 onmouseover="gutterOver(151)"

><td class="source">                });<br></td></tr
><tr
id=sl_svn22_152

 onmouseover="gutterOver(152)"

><td class="source">            }<br></td></tr
><tr
id=sl_svn22_153

 onmouseover="gutterOver(153)"

><td class="source">            // FIXME: Perhaps using $.data would be a better idea?<br></td></tr
><tr
id=sl_svn22_154

 onmouseover="gutterOver(154)"

><td class="source">            options.formTemplate = template;<br></td></tr
><tr
id=sl_svn22_155

 onmouseover="gutterOver(155)"

><td class="source"><br></td></tr
><tr
id=sl_svn22_156

 onmouseover="gutterOver(156)"

><td class="source">            if ($$.attr(&#39;tagName&#39;) == &#39;TR&#39;) {<br></td></tr
><tr
id=sl_svn22_157

 onmouseover="gutterOver(157)"

><td class="source">                // If forms are laid out as table rows, insert the<br></td></tr
><tr
id=sl_svn22_158

 onmouseover="gutterOver(158)"

><td class="source">                // &quot;add&quot; button in a new table row:<br></td></tr
><tr
id=sl_svn22_159

 onmouseover="gutterOver(159)"

><td class="source">                var numCols = $$.eq(0).children().length,   // This is a bit of an assumption :|<br></td></tr
><tr
id=sl_svn22_160

 onmouseover="gutterOver(160)"

><td class="source">                    buttonRow = $(&#39;&lt;tr&gt;&lt;td colspan=&quot;&#39; + numCols + &#39;&quot;&gt;&lt;a class=&quot;&#39; + options.addCssClass + &#39;&quot; href=&quot;javascript:void(0)&quot;&gt;&#39; + options.addText + &#39;&lt;/a&gt;&lt;/tr&gt;&#39;)<br></td></tr
><tr
id=sl_svn22_161

 onmouseover="gutterOver(161)"

><td class="source">                                .addClass(options.formCssClass + &#39;-add&#39;);<br></td></tr
><tr
id=sl_svn22_162

 onmouseover="gutterOver(162)"

><td class="source">                $$.parent().append(buttonRow);<br></td></tr
><tr
id=sl_svn22_163

 onmouseover="gutterOver(163)"

><td class="source">                if (hideAddButton) buttonRow.hide();<br></td></tr
><tr
id=sl_svn22_164

 onmouseover="gutterOver(164)"

><td class="source">                addButton = buttonRow.find(&#39;a&#39;);<br></td></tr
><tr
id=sl_svn22_165

 onmouseover="gutterOver(165)"

><td class="source">            } else {<br></td></tr
><tr
id=sl_svn22_166

 onmouseover="gutterOver(166)"

><td class="source">                // Otherwise, insert it immediately after the last form:<br></td></tr
><tr
id=sl_svn22_167

 onmouseover="gutterOver(167)"

><td class="source">                $$.filter(&#39;:last&#39;).after(&#39;&lt;a class=&quot;&#39; + options.addCssClass + &#39;&quot; href=&quot;javascript:void(0)&quot;&gt;&#39; + options.addText + &#39;&lt;/a&gt;&#39;);<br></td></tr
><tr
id=sl_svn22_168

 onmouseover="gutterOver(168)"

><td class="source">                addButton = $$.filter(&#39;:last&#39;).next();<br></td></tr
><tr
id=sl_svn22_169

 onmouseover="gutterOver(169)"

><td class="source">                if (hideAddButton) addButton.hide();<br></td></tr
><tr
id=sl_svn22_170

 onmouseover="gutterOver(170)"

><td class="source">            }<br></td></tr
><tr
id=sl_svn22_171

 onmouseover="gutterOver(171)"

><td class="source">            addButton.click(function() {<br></td></tr
><tr
id=sl_svn22_172

 onmouseover="gutterOver(172)"

><td class="source">                var formCount = parseInt(totalForms.val()),<br></td></tr
><tr
id=sl_svn22_173

 onmouseover="gutterOver(173)"

><td class="source">                    row = options.formTemplate.clone(true).removeClass(&#39;formset-custom-template&#39;),<br></td></tr
><tr
id=sl_svn22_174

 onmouseover="gutterOver(174)"

><td class="source">                    buttonRow = $($(this).parents(&#39;tr.&#39; + options.formCssClass + &#39;-add&#39;).get(0) || this);<br></td></tr
><tr
id=sl_svn22_175

 onmouseover="gutterOver(175)"

><td class="source">                applyExtraClasses(row, formCount);<br></td></tr
><tr
id=sl_svn22_176

 onmouseover="gutterOver(176)"

><td class="source">                row.insertBefore(buttonRow).show();<br></td></tr
><tr
id=sl_svn22_177

 onmouseover="gutterOver(177)"

><td class="source">                row.find(childElementSelector).each(function() {<br></td></tr
><tr
id=sl_svn22_178

 onmouseover="gutterOver(178)"

><td class="source">                    updateElementIndex($(this), options.prefix, formCount);<br></td></tr
><tr
id=sl_svn22_179

 onmouseover="gutterOver(179)"

><td class="source">                });<br></td></tr
><tr
id=sl_svn22_180

 onmouseover="gutterOver(180)"

><td class="source">                totalForms.val(formCount + 1);<br></td></tr
><tr
id=sl_svn22_181

 onmouseover="gutterOver(181)"

><td class="source">                // Check if we&#39;ve exceeded the maximum allowed number of forms:<br></td></tr
><tr
id=sl_svn22_182

 onmouseover="gutterOver(182)"

><td class="source">                if (!showAddButton()) buttonRow.hide();<br></td></tr
><tr
id=sl_svn22_183

 onmouseover="gutterOver(183)"

><td class="source">                // If a post-add callback was supplied, call it with the added form:<br></td></tr
><tr
id=sl_svn22_184

 onmouseover="gutterOver(184)"

><td class="source">                if (options.added) options.added(row);<br></td></tr
><tr
id=sl_svn22_185

 onmouseover="gutterOver(185)"

><td class="source">                return false;<br></td></tr
><tr
id=sl_svn22_186

 onmouseover="gutterOver(186)"

><td class="source">            });<br></td></tr
><tr
id=sl_svn22_187

 onmouseover="gutterOver(187)"

><td class="source">        }<br></td></tr
><tr
id=sl_svn22_188

 onmouseover="gutterOver(188)"

><td class="source"><br></td></tr
><tr
id=sl_svn22_189

 onmouseover="gutterOver(189)"

><td class="source">        return $$;<br></td></tr
><tr
id=sl_svn22_190

 onmouseover="gutterOver(190)"

><td class="source">    }<br></td></tr
><tr
id=sl_svn22_191

 onmouseover="gutterOver(191)"

><td class="source"><br></td></tr
><tr
id=sl_svn22_192

 onmouseover="gutterOver(192)"

><td class="source">    /* Setup plugin defaults */<br></td></tr
><tr
id=sl_svn22_193

 onmouseover="gutterOver(193)"

><td class="source">    $.fn.formset.defaults = {<br></td></tr
><tr
id=sl_svn22_194

 onmouseover="gutterOver(194)"

><td class="source">        prefix: &#39;form&#39;,                  // The form prefix for your django formset<br></td></tr
><tr
id=sl_svn22_195

 onmouseover="gutterOver(195)"

><td class="source">        formTemplate: null,              // The jQuery selection cloned to generate new form instances<br></td></tr
><tr
id=sl_svn22_196

 onmouseover="gutterOver(196)"

><td class="source">        addText: &#39;add another&#39;,          // Text for the add link<br></td></tr
><tr
id=sl_svn22_197

 onmouseover="gutterOver(197)"

><td class="source">        deleteText: &#39;remove&#39;,            // Text for the delete link<br></td></tr
><tr
id=sl_svn22_198

 onmouseover="gutterOver(198)"

><td class="source">        addCssClass: &#39;add-row&#39;,          // CSS class applied to the add link<br></td></tr
><tr
id=sl_svn22_199

 onmouseover="gutterOver(199)"

><td class="source">        deleteCssClass: &#39;delete-row&#39;,    // CSS class applied to the delete link<br></td></tr
><tr
id=sl_svn22_200

 onmouseover="gutterOver(200)"

><td class="source">        formCssClass: &#39;dynamic-form&#39;,    // CSS class applied to each form in a formset<br></td></tr
><tr
id=sl_svn22_201

 onmouseover="gutterOver(201)"

><td class="source">        extraClasses: [],                // Additional CSS classes, which will be applied to each form in turn<br></td></tr
><tr
id=sl_svn22_202

 onmouseover="gutterOver(202)"

><td class="source">        keepFieldValues: &#39;&#39;,             // jQuery selector for fields whose values should be kept when the form is cloned<br></td></tr
><tr
id=sl_svn22_203

 onmouseover="gutterOver(203)"

><td class="source">        added: null,                     // Function called each time a new form is added<br></td></tr
><tr
id=sl_svn22_204

 onmouseover="gutterOver(204)"

><td class="source">        removed: null                    // Function called each time a form is deleted<br></td></tr
><tr
id=sl_svn22_205

 onmouseover="gutterOver(205)"

><td class="source">    };<br></td></tr
><tr
id=sl_svn22_206

 onmouseover="gutterOver(206)"

><td class="source">})(jQuery)<br></td></tr
></table></pre>
<pre><table width="100%"><tr class="cursor_stop cursor_hidden"><td></td></tr></table></pre>
</td>
</tr></table>

 
<script type="text/javascript">
 var lineNumUnderMouse = -1;
 
 function gutterOver(num) {
 gutterOut();
 var newTR = document.getElementById('gr_svn22_' + num);
 if (newTR) {
 newTR.className = 'undermouse';
 }
 lineNumUnderMouse = num;
 }
 function gutterOut() {
 if (lineNumUnderMouse != -1) {
 var oldTR = document.getElementById(
 'gr_svn22_' + lineNumUnderMouse);
 if (oldTR) {
 oldTR.className = '';
 }
 lineNumUnderMouse = -1;
 }
 }
 var numsGenState = {table_base_id: 'nums_table_'};
 var srcGenState = {table_base_id: 'src_table_'};
 var alignerRunning = false;
 var startOver = false;
 function setLineNumberHeights() {
 if (alignerRunning) {
 startOver = true;
 return;
 }
 numsGenState.chunk_id = 0;
 numsGenState.table = document.getElementById('nums_table_0');
 numsGenState.row_num = 0;
 if (!numsGenState.table) {
 return; // Silently exit if no file is present.
 }
 srcGenState.chunk_id = 0;
 srcGenState.table = document.getElementById('src_table_0');
 srcGenState.row_num = 0;
 alignerRunning = true;
 continueToSetLineNumberHeights();
 }
 function rowGenerator(genState) {
 if (genState.row_num < genState.table.rows.length) {
 var currentRow = genState.table.rows[genState.row_num];
 genState.row_num++;
 return currentRow;
 }
 var newTable = document.getElementById(
 genState.table_base_id + (genState.chunk_id + 1));
 if (newTable) {
 genState.chunk_id++;
 genState.row_num = 0;
 genState.table = newTable;
 return genState.table.rows[0];
 }
 return null;
 }
 var MAX_ROWS_PER_PASS = 1000;
 function continueToSetLineNumberHeights() {
 var rowsInThisPass = 0;
 var numRow = 1;
 var srcRow = 1;
 while (numRow && srcRow && rowsInThisPass < MAX_ROWS_PER_PASS) {
 numRow = rowGenerator(numsGenState);
 srcRow = rowGenerator(srcGenState);
 rowsInThisPass++;
 if (numRow && srcRow) {
 if (numRow.offsetHeight != srcRow.offsetHeight) {
 numRow.firstChild.style.height = srcRow.offsetHeight + 'px';
 }
 }
 }
 if (rowsInThisPass >= MAX_ROWS_PER_PASS) {
 setTimeout(continueToSetLineNumberHeights, 10);
 } else {
 alignerRunning = false;
 if (startOver) {
 startOver = false;
 setTimeout(setLineNumberHeights, 500);
 }
 }
 }
 function initLineNumberHeights() {
 // Do 2 complete passes, because there can be races
 // between this code and prettify.
 startOver = true;
 setTimeout(setLineNumberHeights, 250);
 window.onresize = setLineNumberHeights;
 }
 initLineNumberHeights();
</script>

 
 
 <div id="log">
 <div style="text-align:right">
 <a class="ifCollapse" href="#" onclick="_toggleMeta(this); return false">Show details</a>
 <a class="ifExpand" href="#" onclick="_toggleMeta(this); return false">Hide details</a>
 </div>
 <div class="ifExpand">
 
 
 <div class="pmeta_bubble_bg" style="border:1px solid white">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <div id="changelog">
 <p>Change log</p>
 <div>
 <a href="/p/django-dynamic-formset/source/detail?spec=svn22&amp;r=16">r16</a>
 by stan.madueke
 on Apr 29, 2011
 &nbsp; <a href="/p/django-dynamic-formset/source/diff?spec=svn22&r=16&amp;format=side&amp;path=/trunk/src/jquery.formset.js&amp;old_path=/trunk/src/jquery.formset.js&amp;old=15">Diff</a>
 </div>
 <pre>Fixed <a title="Working with django-uni-form" class=closed_ref href="/p/django-dynamic-formset/issues/detail?id=13"> Issue 13 </a>
Updated RegExp so plugin works better with
`Formset.empty_form` in Django 1.2+
Added a few new examples</pre>
 </div>
 
 
 
 
 
 
 <script type="text/javascript">
 var detail_url = '/p/django-dynamic-formset/source/detail?r=16&spec=svn22';
 var publish_url = '/p/django-dynamic-formset/source/detail?r=16&spec=svn22#publish';
 // describe the paths of this revision in javascript.
 var changed_paths = [];
 var changed_urls = [];
 
 changed_paths.push('/trunk/demo/example/forms.py');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/demo/example/forms.py?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/demo/example/urls.py');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/demo/example/urls.py?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/demo/example/views.py');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/demo/example/views.py?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/demo/settings.py');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/demo/settings.py?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/demo/static/images/loading.gif');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/demo/static/images/loading.gif?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/demo/static/js/jquery.formset.js');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/demo/static/js/jquery.formset.js?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/demo/templates/example/empty-form.html');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/demo/templates/example/empty-form.html?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/demo/templates/example/form-template.html');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/demo/templates/example/form-template.html?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/demo/templates/example/inline-formset-django-ajax-select.html');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/demo/templates/example/inline-formset-django-ajax-select.html?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/demo/templates/example/inline-formset.html');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/demo/templates/example/inline-formset.html?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/demo/templates/index.html');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/demo/templates/index.html?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/demo/urls.py');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/demo/urls.py?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/docs/usage.txt');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/docs/usage.txt?r\x3d16\x26spec\x3dsvn22');
 
 
 changed_paths.push('/trunk/src/jquery.formset.js');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/src/jquery.formset.js?r\x3d16\x26spec\x3dsvn22');
 
 var selected_path = '/trunk/src/jquery.formset.js';
 
 
 changed_paths.push('/trunk/src/jquery.formset.min.js');
 changed_urls.push('/p/django-dynamic-formset/source/browse/trunk/src/jquery.formset.min.js?r\x3d16\x26spec\x3dsvn22');
 
 
 function getCurrentPageIndex() {
 for (var i = 0; i < changed_paths.length; i++) {
 if (selected_path == changed_paths[i]) {
 return i;
 }
 }
 }
 function getNextPage() {
 var i = getCurrentPageIndex();
 if (i < changed_paths.length - 1) {
 return changed_urls[i + 1];
 }
 return null;
 }
 function getPreviousPage() {
 var i = getCurrentPageIndex();
 if (i > 0) {
 return changed_urls[i - 1];
 }
 return null;
 }
 function gotoNextPage() {
 var page = getNextPage();
 if (!page) {
 page = detail_url;
 }
 window.location = page;
 }
 function gotoPreviousPage() {
 var page = getPreviousPage();
 if (!page) {
 page = detail_url;
 }
 window.location = page;
 }
 function gotoDetailPage() {
 window.location = detail_url;
 }
 function gotoPublishPage() {
 window.location = publish_url;
 }
</script>

 
 <style type="text/css">
 #review_nav {
 border-top: 3px solid white;
 padding-top: 6px;
 margin-top: 1em;
 }
 #review_nav td {
 vertical-align: middle;
 }
 #review_nav select {
 margin: .5em 0;
 }
 </style>
 <div id="review_nav">
 <table><tr><td>Go to:&nbsp;</td><td>
 <select name="files_in_rev" onchange="window.location=this.value">
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/demo/example/forms.py?r=16&amp;spec=svn22"
 
 >/trunk/demo/example/forms.py</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/demo/example/urls.py?r=16&amp;spec=svn22"
 
 >/trunk/demo/example/urls.py</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/demo/example/views.py?r=16&amp;spec=svn22"
 
 >/trunk/demo/example/views.py</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/demo/settings.py?r=16&amp;spec=svn22"
 
 >/trunk/demo/settings.py</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/demo/static/images/loading.gif?r=16&amp;spec=svn22"
 
 >...k/demo/static/images/loading.gif</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/demo/static/js/jquery.formset.js?r=16&amp;spec=svn22"
 
 >...demo/static/js/jquery.formset.js</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/demo/templates/example/empty-form.html?r=16&amp;spec=svn22"
 
 >...emplates/example/empty-form.html</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/demo/templates/example/form-template.html?r=16&amp;spec=svn22"
 
 >...lates/example/form-template.html</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/demo/templates/example/inline-formset-django-ajax-select.html?r=16&amp;spec=svn22"
 
 >...-formset-django-ajax-select.html</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/demo/templates/example/inline-formset.html?r=16&amp;spec=svn22"
 
 >...ates/example/inline-formset.html</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/demo/templates/index.html?r=16&amp;spec=svn22"
 
 >/trunk/demo/templates/index.html</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/demo/urls.py?r=16&amp;spec=svn22"
 
 >/trunk/demo/urls.py</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/docs/usage.txt?r=16&amp;spec=svn22"
 
 >/trunk/docs/usage.txt</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/src/jquery.formset.js?r=16&amp;spec=svn22"
 selected="selected"
 >/trunk/src/jquery.formset.js</option>
 
 <option value="/p/django-dynamic-formset/source/browse/trunk/src/jquery.formset.min.js?r=16&amp;spec=svn22"
 
 >/trunk/src/jquery.formset.min.js</option>
 
 </select>
 </td></tr></table>
 
 
 <div id="review_instr" class="closed">
 <a class="ifOpened" href="/p/django-dynamic-formset/source/detail?r=16&spec=svn22#publish">Publish your comments</a>
 <div class="ifClosed">Double click a line to add a comment</div>
 </div>
 
 </div>
 
 
 </div>
 <div class="round1"></div>
 <div class="round2"></div>
 <div class="round4"></div>
 </div>
 <div class="pmeta_bubble_bg" style="border:1px solid white">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <div id="older_bubble">
 <p>Older revisions</p>
 
 
 <div class="closed" style="margin-bottom:3px;" >
 <a class="ifClosed" onclick="return _toggleHidden(this)"><img src="http://www.gstatic.com/codesite/ph/images/plus.gif" ></a>
 <a class="ifOpened" onclick="return _toggleHidden(this)"><img src="http://www.gstatic.com/codesite/ph/images/minus.gif" ></a>
 <a href="/p/django-dynamic-formset/source/detail?spec=svn22&r=15">r15</a>
 by stan.madueke
 on Apr 20, 2011
 &nbsp; <a href="/p/django-dynamic-formset/source/diff?spec=svn22&r=15&amp;format=side&amp;path=/trunk/src/jquery.formset.js&amp;old_path=/trunk/src/jquery.formset.js&amp;old=14">Diff</a>
 <br>
 <pre class="ifOpened">Closed <a title="Few formsets on one page" class=closed_ref href="/p/django-dynamic-formset/issues/detail?id=23"> Issue 23 </a>
Fixed Issues 26, 16, 15, 14 and 9</pre>
 </div>
 
 <div class="closed" style="margin-bottom:3px;" >
 <a class="ifClosed" onclick="return _toggleHidden(this)"><img src="http://www.gstatic.com/codesite/ph/images/plus.gif" ></a>
 <a class="ifOpened" onclick="return _toggleHidden(this)"><img src="http://www.gstatic.com/codesite/ph/images/minus.gif" ></a>
 <a href="/p/django-dynamic-formset/source/detail?spec=svn22&r=14">r14</a>
 by stan.madueke
 on Jul 3, 2010
 &nbsp; <a href="/p/django-dynamic-formset/source/diff?spec=svn22&r=14&amp;format=side&amp;path=/trunk/src/jquery.formset.js&amp;old_path=/trunk/src/jquery.formset.js&amp;old=12">Diff</a>
 <br>
 <pre class="ifOpened">- Added support for the MAX_NUM_FORMS
parameter, added to the management
form in Django 1.2
- Fixed the autocomplete example
- Switched to Google's Closure
...</pre>
 </div>
 
 <div class="closed" style="margin-bottom:3px;" >
 <a class="ifClosed" onclick="return _toggleHidden(this)"><img src="http://www.gstatic.com/codesite/ph/images/plus.gif" ></a>
 <a class="ifOpened" onclick="return _toggleHidden(this)"><img src="http://www.gstatic.com/codesite/ph/images/minus.gif" ></a>
 <a href="/p/django-dynamic-formset/source/detail?spec=svn22&r=12">r12</a>
 by stan.madueke
 on Apr 12, 2010
 &nbsp; <a href="/p/django-dynamic-formset/source/diff?spec=svn22&r=12&amp;format=side&amp;path=/trunk/src/jquery.formset.js&amp;old_path=/trunk/src/jquery.formset.js&amp;old=10">Diff</a>
 <br>
 <pre class="ifOpened">Finished documentation for 1.2</pre>
 </div>
 
 
 <a href="/p/django-dynamic-formset/source/list?path=/trunk/src/jquery.formset.js&start=16">All revisions of this file</a>
 </div>
 </div>
 <div class="round1"></div>
 <div class="round2"></div>
 <div class="round4"></div>
 </div>
 
 <div class="pmeta_bubble_bg" style="border:1px solid white">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <div id="fileinfo_bubble">
 <p>File info</p>
 
 <div>Size: 11552 bytes,
 206 lines</div>
 
 <div><a href="//django-dynamic-formset.googlecode.com/svn/trunk/src/jquery.formset.js">View raw file</a></div>
 </div>
 
 </div>
 <div class="round1"></div>
 <div class="round2"></div>
 <div class="round4"></div>
 </div>
 </div>
 </div>


</div>

</div>
</div>

<script src="http://www.gstatic.com/codesite/ph/3197964839662303775/js/prettify/prettify.js"></script>
<script type="text/javascript">prettyPrint();</script>


<script src="http://www.gstatic.com/codesite/ph/3197964839662303775/js/source_file_scripts.js"></script>

 <script type="text/javascript" src="http://www.gstatic.com/codesite/ph/3197964839662303775/js/kibbles.js"></script>
 <script type="text/javascript">
 var lastStop = null;
 var initialized = false;
 
 function updateCursor(next, prev) {
 if (prev && prev.element) {
 prev.element.className = 'cursor_stop cursor_hidden';
 }
 if (next && next.element) {
 next.element.className = 'cursor_stop cursor';
 lastStop = next.index;
 }
 }
 
 function pubRevealed(data) {
 updateCursorForCell(data.cellId, 'cursor_stop cursor_hidden');
 if (initialized) {
 reloadCursors();
 }
 }
 
 function draftRevealed(data) {
 updateCursorForCell(data.cellId, 'cursor_stop cursor_hidden');
 if (initialized) {
 reloadCursors();
 }
 }
 
 function draftDestroyed(data) {
 updateCursorForCell(data.cellId, 'nocursor');
 if (initialized) {
 reloadCursors();
 }
 }
 function reloadCursors() {
 kibbles.skipper.reset();
 loadCursors();
 if (lastStop != null) {
 kibbles.skipper.setCurrentStop(lastStop);
 }
 }
 // possibly the simplest way to insert any newly added comments
 // is to update the class of the corresponding cursor row,
 // then refresh the entire list of rows.
 function updateCursorForCell(cellId, className) {
 var cell = document.getElementById(cellId);
 // we have to go two rows back to find the cursor location
 var row = getPreviousElement(cell.parentNode);
 row.className = className;
 }
 // returns the previous element, ignores text nodes.
 function getPreviousElement(e) {
 var element = e.previousSibling;
 if (element.nodeType == 3) {
 element = element.previousSibling;
 }
 if (element && element.tagName) {
 return element;
 }
 }
 function loadCursors() {
 // register our elements with skipper
 var elements = CR_getElements('*', 'cursor_stop');
 var len = elements.length;
 for (var i = 0; i < len; i++) {
 var element = elements[i]; 
 element.className = 'cursor_stop cursor_hidden';
 kibbles.skipper.append(element);
 }
 }
 function toggleComments() {
 CR_toggleCommentDisplay();
 reloadCursors();
 }
 function keysOnLoadHandler() {
 // setup skipper
 kibbles.skipper.addStopListener(
 kibbles.skipper.LISTENER_TYPE.PRE, updateCursor);
 // Set the 'offset' option to return the middle of the client area
 // an option can be a static value, or a callback
 kibbles.skipper.setOption('padding_top', 50);
 // Set the 'offset' option to return the middle of the client area
 // an option can be a static value, or a callback
 kibbles.skipper.setOption('padding_bottom', 100);
 // Register our keys
 kibbles.skipper.addFwdKey("n");
 kibbles.skipper.addRevKey("p");
 kibbles.keys.addKeyPressListener(
 'u', function() { window.location = detail_url; });
 kibbles.keys.addKeyPressListener(
 'r', function() { window.location = detail_url + '#publish'; });
 
 kibbles.keys.addKeyPressListener('j', gotoNextPage);
 kibbles.keys.addKeyPressListener('k', gotoPreviousPage);
 
 
 kibbles.keys.addKeyPressListener('h', toggleComments);
 
 }
 </script>
<script src="http://www.gstatic.com/codesite/ph/3197964839662303775/js/code_review_scripts.js"></script>
<script type="text/javascript">
 function showPublishInstructions() {
 var element = document.getElementById('review_instr');
 if (element) {
 element.className = 'opened';
 }
 }
 var codereviews;
 function revsOnLoadHandler() {
 // register our source container with the commenting code
 var paths = {'svn22': '/trunk/src/jquery.formset.js'}
 codereviews = CR_controller.setup(
 {"assetVersionPath": "http://www.gstatic.com/codesite/ph/3197964839662303775", "profileUrl": "/u/jmjacquet@gmail.com/", "projectHomeUrl": "/p/django-dynamic-formset", "token": "ABZ6GAeQ5SSRchth9mbxnKeigZ0COlBM5Q:1432077715372", "relativeBaseUrl": "", "domainName": null, "assetHostPath": "http://www.gstatic.com/codesite/ph", "projectName": "django-dynamic-formset", "loggedInUserEmail": "jmjacquet@gmail.com"}, '', 'svn22', paths,
 CR_BrowseIntegrationFactory);
 
 // register our source container with the commenting code
 // in this case we're registering the container and the revison
 // associated with the contianer which may be the primary revision
 // or may be a previous revision against which the primary revision
 // of the file is being compared.
 codereviews.registerSourceContainer(document.getElementById('lines'), 'svn22');
 
 codereviews.registerActivityListener(CR_ActivityType.REVEAL_DRAFT_PLATE, showPublishInstructions);
 
 codereviews.registerActivityListener(CR_ActivityType.REVEAL_PUB_PLATE, pubRevealed);
 codereviews.registerActivityListener(CR_ActivityType.REVEAL_DRAFT_PLATE, draftRevealed);
 codereviews.registerActivityListener(CR_ActivityType.DISCARD_DRAFT_COMMENT, draftDestroyed);
 
 
 
 
 
 
 
 var initialized = true;
 reloadCursors();
 }
 window.onload = function() {keysOnLoadHandler(); revsOnLoadHandler();};

</script>
<script type="text/javascript" src="http://www.gstatic.com/codesite/ph/3197964839662303775/js/dit_scripts.js"></script>

 
 
 
 <script type="text/javascript" src="http://www.gstatic.com/codesite/ph/3197964839662303775/js/ph_core.js"></script>
 
 
 
 
</div> 

<div id="footer" dir="ltr">
 <div class="text">
 <a href="/projecthosting/terms.html">Terms</a> -
 <a href="http://www.google.com/privacy.html">Privacy</a> -
 <a href="/p/support/">Project Hosting Help</a>
 </div>
</div>
 <div class="hostedBy" style="margin-top: -20px;">
 <span style="vertical-align: top;">Powered by <a href="http://code.google.com/projecthosting/">Google Project Hosting</a></span>
 </div>

 
 


 
 </body>
</html>

