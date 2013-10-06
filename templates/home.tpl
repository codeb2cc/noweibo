{% extends "base.tpl" %}

{% block css %}
<link rel="stylesheet" href="/public/css/app.css">
{% end %}

{% block body %}
<!-- Fixed navbar -->
<div class="navbar navbar-default navbar-fixed-top">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">Noweibo | 莫微薄</a>
      <span class="badge navbar-brand-beta">BETA</span>
    </div>
    <div class="collapse navbar-collapse navbar-right">
      <ul class="nav navbar-nav">
        <li><a data-toggle="modal" href="#about">关于</a></li>
      </ul>
    </div><!--/.nav-collapse -->
  </div>
</div>

<div class="container" ng-show="user" style="display: none;">
  <div class="row">
    <div class="col-md-3">
      <div id="user_info">
        <div id="user_avatar">
          <img ng-src="{{! user.avatar_large }}" alt="{{! user.name }}" class="img-thumbnail">
        </div>
        <h2 ng-bind="user.name"></h2>
        <p ng-bind="user.description"></p>
      </div>
      <div id="user_control" class="btn-group">
        <button type="button" class="btn btn-default disabled" title="暂不支持该功能">
          <span class="glyphicon glyphicon-envelope"></span> 消息提醒
        </button>
        <button type="button" class="btn btn-default" title="自动删除转发数500以上的微博" ng-class="optionDeleteBtnClass()" ng-click="updateUserOptions('delete')">
          <span class="glyphicon glyphicon-trash"></span> 自动删除
        </button>
        <button type="button" class="btn btn-success" title="刷新微博数据" ng-click="syncWeibo()">
          <span class="glyphicon glyphicon-refresh"></span>
        </button>
      </div>
      <div id="user_status">
        <ul class="list-group">
          <li class="list-group-item"><span class="badge" ng-bind="user.friends_count"></span>关注</li>
          <li class="list-group-item"><span class="badge" ng-bind="user.followers_count"></span>粉丝</li>
          <li class="list-group-item"><span class="badge" ng-bind="user.statuses_count"></span>微博</li>
        </ul>
      </div>
    </div>
    <div class="col-md-9">
      <div id="user_tool">
        <div class="btn-group">
          <button type="button" class="btn btn-default" ng-class="orderBtnClass('time')" ng-click="changeOrder('time')">
            <span class="glyphicon glyphicon-time"></span> 时间排序
          </button>
          <button type="button" class="btn btn-default" ng-class="orderBtnClass('repost')" ng-click="changeOrder('repost')">
            <span class="glyphicon glyphicon-export"></span> 转发排序
          </button>
          <button type="button" class="btn btn-default" ng-class="orderBtnClass('comment')" ng-click="changeOrder('comment')">
            <span class="glyphicon glyphicon-comment"></span> 评论排序
          </button>
        </div>
        <div class="btn-group" id="user_pagination">
          <button type="button" class="btn btn-default" ng-repeat="i in pages" ng-class="pageBtnClass($index)" ng-click="changePage($index)">{{! $index + 1 }}</button>
        </div>
      </div>
      <div id="user_weibo">
        <ul class="media-list">
          <li class="media" ng-repeat="weibo in weibos | orderBy:orderFilter():true" ng-show="pageFilter($index)">
            <div class="media-body">
              <h5 class="media-heading text-muted">
                {{! weibo.create_date * 1000 | date:'medium' }}
              </h5>
              <a href="/weibo/redirect?wid={{! weibo.wid }}" target="_blank"><span class="glyphicon glyphicon-new-window" title="查看原微博"></span></a>
              <p ng-bind="weibo.text" com-short-url></p>
            </div>
            <div class="media-append clearfix">
              <span title="转发数" ng-bind-html-unsafe="weibo.reposts_count | colorFilter"></span>
              <span title="评论数" ng-bind-html-unsafe="weibo.comments_count | colorFilter"></span>
              <span title="表态数" ng-bind-html-unsafe="weibo.attitudes_count | colorFilter"></span>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>

  <hr>

  {% include "about.tpl" %}

  {% include "footer.tpl" %}
</div> <!-- /container -->
{% end %}

{% block js %}
<script src="/public/js/home.js"></script>
{% end %}
