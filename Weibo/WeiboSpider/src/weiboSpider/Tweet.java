package weiboSpider;

import java.io.Serializable;
import java.util.Date;


public class Tweet implements Serializable,Comparable<Tweet> {
	private static final long serialVersionUID = 578920508456872682L;
	//微博ID
	long id;
	//微博创建时间
	Date createDate;
	//微博内容
	String text;
	//转发与评论数
	int reposts;
	int comments;
	//微博发布者id
	long uid;
	//是否是转发的微博
	boolean isRetweet;
	//原微博的ID
	long sid;
	public Tweet(long id, Date cd, String text, int reposts, int comments, long uid, boolean isRetweet, long sid) {
		this.id = id;
		this.createDate = cd;
		this.text = text;
		this.reposts = reposts;
		this.comments = comments;
		this.uid = uid;
		this.isRetweet = isRetweet;
		this.sid = sid;
	}
	public boolean equals(Object o){
		return o instanceof Tweet && (id==((Tweet)o).id);
	}
	//！！注意！！此处排序为逆序，id越大排在越靠前的位置
	public int compareTo(Tweet t) {
		long diff = this.id-t.id;
		return (diff>0)?-1:((diff==0)?0:1);
	}
	//可修改属性，转发数，评论数，源微博id
	public void setReposts(int reposts) {
		this.reposts = reposts;
	}
	public int getReposts() {
		return reposts;
	}
	public void setComments(int comments) {
		this.comments = comments;
	}
	public int getComments() {
		return comments;
	}
	public void setSID(long sid) {
		this.sid =sid;
	}
	public long getSID() {
		return sid;
	}
	//不可修改属性，作者id，微博id，是否是转发微博，微博内容
	public long getUID(){
		return uid;
	}
	public long getID() {
		return id;
	}
	public boolean isRetweet() {
		return isRetweet;
	}
	public String getText() {
		return text;
	}
}
