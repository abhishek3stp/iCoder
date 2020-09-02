from django.shortcuts import render, redirect
from blog.models import Post, BlogComment
from  django.contrib import messages
from blog.templatetags import extras


# Home page of blog
def blogHome(request):
    allPosts = Post.objects.all()
    params = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', params)


# Blog page for full view of blog
def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)

    # Make a dictionary for comment to there replies
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    params = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, 'blog/blogPost.html', params)


# Posting comments and there replies
def postComment(request):
    if request.method=="POST":
        comment = request.POST.get("comment")
        postSno = request.POST.get("postSno")
        parentSno = request.POST.get("parentSno")
        user = request.user
        post = Post.objects.get(sno=postSno)
        
        # Check whether it is a comment or reply
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            messages.success(request, "Your comment has been posted successfully.")
        
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            messages.success(request, "Your reply has been posted successfully.")
        
        comment.save()
    return redirect(f"/blog/{post.slug}")
