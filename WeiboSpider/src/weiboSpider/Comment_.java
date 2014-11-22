package weiboSpider;

import java.util.Date;

import weibo4j.model.Comment;
import weibo4j.model.Status;
import weibo4j.model.User;

public class Comment_ implements java.io.Serializable, Comparable<Comment_>{
	private static final long serialVersionUID = 1272011191123456589L;
	private Date createdAt;                    //评论时间
	private long id;                           //评论id
	private String text;                       //评论内容
	private long uid;                  //User id
	private long sid;              //原微博 id
	
	public Comment_(long id, long sid, long uid, String text, Date createdAt) {
		this.id = id;
		this.sid = sid;
		this.uid = uid;
		this.text = text;
		this.createdAt = createdAt;
	}
	
	public long getID() {
		return id;		
	}
	
	public long getUID() {
		return uid;
	}
	
	public long getSID() {
		return sid;
	}
	
	public String getText() {
		return text;
	}
	
	public Date createdAt() {
		return createdAt;
	}
	
	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + (int) (id ^ (id >>> 32));
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Comment_ other = (Comment_) obj;
		if (id != other.id)
			return false;
		return true;
	}
	
	@Override
	public int compareTo(Comment_ c) {
		if(this.sid>c.sid) return -1;
		if(this.sid<c.sid) return 1;
		if(this.id>c.id) return -1;
		if(this.id<c.id) return 1;
		return 0;
	}
}
