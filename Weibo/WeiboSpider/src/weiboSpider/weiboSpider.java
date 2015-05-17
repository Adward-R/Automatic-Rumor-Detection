package weiboSpider;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.PrintWriter;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.TreeSet;

import weibo4j.Comments;
import weibo4j.Timeline;
import weibo4j.model.Comment;
import weibo4j.model.Paging;
import weibo4j.model.Status;
import weibo4j.model.User;
import weibo4j.model.WeiboException;
import weibo4j.org.json.JSONArray;

public class weiboSpider {
	//String token = "2.00jcof_Cq3jyKE7ddb08a8440dj2qo";
	String token;
	static final int count = 200;
	TreeSet<Tweet> tweetSet = new TreeSet<Tweet>();
	TreeSet<Comment_> commentSet = new TreeSet<Comment_>();
	HashSet<Status> statusSet = new HashSet<Status>();
	HashSet<User> userSet = new HashSet<User>();
	public static void main(String[] args){
		weiboSpider ws = new weiboSpider("2.00jcof_Cq3jyKE7ddb08a8440dj2qo");
		String dir = "D:\\Scholar\\school\\work\\rumor-news classification\\";
		//ws.testGetReposts("3667867842829486");//test mid 1
		//ws.testGetReposts("3684753900918353");
		//ws.getTree(args[0],true);
		/*ws.getTree(args[0], true);
		ws.saveResult(dir, args[0]);*/
		ws.restoreResult(dir, args[0]);
		try{
			PrintWriter pw = new PrintWriter(dir+args[0]+".txt");
			for(Tweet t:ws.tweetSet) {
				pw.println(t.getID()+" "+t.text);
			}
			pw.close();
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public weiboSpider(String accessToken) {
		token = accessToken;
	}
	
	//获取一条微博的转发树，同时获取评论和参与用户信息
	public void getTree(String id, boolean isMID) {
		Timeline tl = new Timeline();
		Comments cm = new Comments();
		tl.setToken(token);
		cm.setToken(token);
		//如果提供的是mid，先转换成id
		if(isMID) {
			try{
				id = tl.QueryId(id, 1, 0).getString("id");
			}catch(WeiboException e) {
				e.printStackTrace();
				if(e.getErrorCode()==10002) {
					try {
						Thread.sleep(1000*60*5);
					} catch (InterruptedException e1) {
						e1.printStackTrace();
					}
				}
			}catch(Exception e) {
				e.printStackTrace();
			}
		}
		try{
			//首先找到根节点，即原始微博
			Status t = tl.showStatus(id);
			if(t.getRetweetedStatus()!=null) {
				t = t.getRetweetedStatus();
			}
			Paging p = new Paging(1, count);
			int totalPage = (t.getRepostsCount()-1)/count+1<2000/count?(t.getRepostsCount()-1)/count+1:2000/count;
			for (int page=1;page<=totalPage;page++) {
				//然后获取其子节点
				p.setPage(page);
				List<Status> ls = tl.getRepostTimeline(t.getId(), p)
						.getStatuses();
				statusSet.addAll(ls);
				Thread.sleep(250);
				for (Status s : ls) {
					//保存微博信息
					saveWeibo(s);
					//保存微博作者信息
					userSet.add(s.getUser());
					long sid = Long.parseLong(s.getId());
					//获取并保存微博的评论
					long commentCount = cm.getCommentById(s.getId()).getTotalNumber();
					Thread.sleep(250);
					long commentPage = (commentCount-1)/count+1<2000/count?(commentCount-1)/count+1:2000/count;
					Paging cp = new Paging(1,count);
					for(int cpage=1;cpage<=commentPage;cpage++) {
						cp.setPage(cpage);
						List<Comment> cl = cm.getCommentById(s.getId(), cp, 0).getComments();
						Thread.sleep(250);
						for(Comment c:cl) {
							saveComment(c, sid);
						}						
					}
				}
			}
			saveWeibo(t);
		}catch(WeiboException e) {
			e.printStackTrace();
			if(e.getErrorCode()==10002) {
				try {
					Thread.sleep(1000*60*5);
				} catch (InterruptedException e1) {
					e1.printStackTrace();
				}
			}
		}catch (InterruptedException e) {
			e.printStackTrace();
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	//构建转发树进行排序，确定每个转发微博的父节点
	public void buildTree() {
		Timeline tl = new Timeline();
		tl.setToken(token);
		boolean isFirst = true;
		for (Tweet t:tweetSet.descendingSet()) {
			if(isFirst) {
				isFirst = false;
				continue;
			}
			
			try {
				int repostsForS = tl.getRepostTimelineIds(
						String.valueOf(t.getID())).getInt("total_number");
				int repostPageForS = (repostsForS-1)/count+1 > 2000/count ?
						(repostsForS-1)/count+1: 2000/count;
				Paging rsp = new Paging(1, count);
				for (int rspage = 1; rspage <= repostPageForS; rspage++) {
					rsp.setPage(rspage);
					JSONArray ids = tl.getRepostTimelineIds(String.valueOf(t.getID()), rsp).getJSONArray("statuses");
					for(int i=0;i<ids.length();i++) {
						
					}
					Thread.sleep(250);
				}
			}catch(WeiboException e) {
				e.printStackTrace();
				if(e.getErrorCode()==10002) {
					try {
						Thread.sleep(1000*60*5);
					} catch (InterruptedException e1) {
						e1.printStackTrace();
					}
				}
			}catch (InterruptedException e) {
				e.printStackTrace();
			}catch(Exception e) {
				e.printStackTrace();
			}
			
		}
	}
	
	//测试接口
	public void testGetReposts(String mid) {
		Timeline tl = new Timeline();
		tl.setToken(token);
		try {
			//通过微博的mid获取id
			String id = tl.QueryId(mid, 1, 0).getString("id");
			//System.out.println(id);
			//通过微博id获取转发列表
			//System.out.println(tl.getRepostTimelineIds(id));
			int p = 1;
			Paging page = new Paging(p, 200);
			File f = new File("D:\\Scholar\\school\\work\\rumor-news classification\\test2.txt");
			if(!f.exists()) f.createNewFile();
			PrintWriter pw = new PrintWriter(f);
			pw.println(tl.getRepostTimeline(id).getTotalNumber());
			pw.println(tl.getRepostTimelineIds(id));
			//测试原创与转发微博的RetweetedStatus
//			pw.println(tl.showStatus("3684687735925871"));
//			pw.println("-----------------status-------------");
//			pw.println("no retweeted="+(tl.showStatus("3684687735925871").getRetweetedStatus()==null));
//			pw.println("-----------------status-------------");
//			pw.println(tl.showStatus(id));
//			pw.println("-----------------status-------------");
//			pw.println();
/*			while(true) {
				StatusWapper reposts = tl.getRepostTimeline(id,page);
				Thread.sleep(250);//sleep for 250 milli
				int i = 0;
				System.out.println("totalnumber = "+reposts.getTotalNumber());
				//test for get reposts
//				for(Status repost:reposts.getStatuses()) {
//					pw.print(repost.getId());
//					pw.print(" ");
//					if(++i%5==0)
//						pw.println();
//				}
//				pw.println();
//				pw.println();
//				pw.println(reposts.getNextCursor());
//				pw.println();
//				pw.flush();
				for(Status repost:reposts.getStatuses()) {
					pw.println(repost);
					pw.println();
				}
				//System.out.println(reposts.getPreviousCursor());
				if(p*200>=2000||p*200>=reposts.getTotalNumber())
					break;
				p++;
				page.setPage(p);
			}*/
			pw.close();
		}catch (WeiboException e) {
			e.printStackTrace();
			if(e.getErrorCode()==10002) {
				try {
					Thread.sleep(1000*60*5);
				} catch (InterruptedException e1) {
					e1.printStackTrace();
				}
			}
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public void saveWeibo(Status weibo) {
		Date d = weibo.getCreatedAt();
		String id = weibo.getId();
		String text = weibo.getText();
		int comments = weibo.getCommentsCount();
		int reposts = weibo.getRepostsCount();
		String uid = weibo.getUser().getId();
		String sourceWeiboId = id;
		boolean isRetweet = false;
		if(weibo.getRetweetedStatus()!=null) {
			isRetweet = true;
			sourceWeiboId = weibo.getRetweetedStatus().getId();
		}
		tweetSet.add(new Tweet(Long.parseLong(id),d,text,reposts,comments,Long.parseLong(uid),isRetweet,Long.parseLong(sourceWeiboId)));
	}
	public void saveComment(Comment c, long sid) {
		long id = c.getId();
		long sid_ = sid;
		long uid = Long.parseLong(c.getUser().getId());
		String text = c.getText();
		Date createdAt = c.getCreatedAt();
		
		commentSet.add(new Comment_(id, sid_, uid, text, createdAt));
	}
	
	public void saveResult(String dir, String id) {
		try {
			ObjectOutputStream out = new ObjectOutputStream(
					new FileOutputStream(dir+id+"_tweet.out"));
			out.writeObject(tweetSet);
			out.close();
			out = new ObjectOutputStream(
					new FileOutputStream(dir+id+"_comment.out"));
			out.writeObject(commentSet);
			out.close();
			out = new ObjectOutputStream(
					new FileOutputStream(dir+id+"_user.out"));
			out.writeObject(userSet);
			out.close();
			/*out = new ObjectOutputStream(
					new FileOutputStream(dir+id+"_status.out"));
			out.writeObject(statusSet);
			out.close();*/	
		}catch(IOException e) {
			e.printStackTrace();
		}
	}
	public void restoreResult(String dir,String id) {
		try {
			ObjectInputStream in = new ObjectInputStream(new FileInputStream(dir+id+"_tweet.out"));
			this.tweetSet = (TreeSet<Tweet>)in.readObject();
			in.close();
			in = new ObjectInputStream(new FileInputStream(dir+id+"_comment.out"));
			this.commentSet = (TreeSet<Comment_>)in.readObject();
			in.close();
			in = new ObjectInputStream(new FileInputStream(dir+id+"_user.out"));
			this.userSet = (HashSet<User>)in.readObject();
			in.close();
			in = new ObjectInputStream(new FileInputStream(dir+id+"_status.out"));
			/*this.statusSet = (HashSet<Status>)in.readObject();
			in.close();	*/
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
}
