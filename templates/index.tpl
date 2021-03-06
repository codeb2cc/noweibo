{% extends "base.tpl" %}

{% block css %}
<link rel="stylesheet" href="/public/css/app.css">
{% end %}

{% block body %}
<!-- Fixed navbar -->
<div class="navbar navbar-default navbar-fixed-top">
  <div class="container">
    <div class="navbar-header">
      <a class="navbar-brand" href="#">Noweibo | 莫微薄</a>
      <span class="badge navbar-brand-beta">BETA</span>
    </div>
    <div class="collapse navbar-collapse">
      <ul class="nav navbar-nav navbar-right">
        <li><a href="/auth/redirect">微博登陆</a></li>
      </ul>
    </div><!--/.nav-collapse -->
  </div>
</div>

<div class="jumbotron">
  <div class="container">
    <h1>Noweibo | 莫微薄</h1>
    <p>微博转发数自动监控，降低自由言论风险成本</p>
    <p><a class="btn btn-primary btn-lg" href="/auth/redirect">开始使用 &raquo;</a></p>
  </div>
</div>
<div class="jumbotron-append" style="display: none;"><p></p></div>

<div class="container" style="margin-top: -5px;">
  <div class="row" ng-show="weibos.length" style="display: none;">
    <div class="col-lg-4 index-weibo" ng-repeat="weibo in weibos">
      <h2><span ng-bind-html-unsafe="weibo.reposts_count | colorFilter" title="转发数"></span> | {{! weibo.uname }}</h2>
      <p com-short-url>{{! weibo.text }}</p>
      <p class="pull-right text-muted">{{! weibo.create_date * 1000 | date:'medium' }}</p>
    </div>
  </div>

  <hr>

  {% include "footer.tpl" %}
</div> <!-- /container -->
{% end %}

{% block js %}
<script src="/public/js/index.js"></script>
{% end %}
