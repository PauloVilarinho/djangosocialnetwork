base_url = 'localhost:8000/'

end_points = [{
"path" :"api/v1/fileloads/",
"description": "post route for loading files to db",
"methods": "post",
},
{
"path" :'profiles',
"description": "list and store profiles",
"methods": "post,get",
},
{
"path" :'profiles/<int:pk>',
"description": "show,update and delete profile",
"methods": "get,put,delete",
},
{
"path" :"profile-post",
"description": "list all profiles with it respectives posts",
"methods": "get",
},
{
"path" :'profile-post/<int:pk>',
"description": "list all posts from an especific profile",
"methods": "get",
},
{
"path" :'posts-comments',
"description": "list all posts with it respectives comments",
"methods": "get",
},
{
"path" :'posts-comments/<int:pk>',
"description": "get all comments from an especific post and the post",
"methods": "get",
},
{
"path" :"posts/<int:pk>/comments",
"description": "list and store comments in an especific post",
"methods": "get,post",
},
{
"path" :'posts/<int:post_pk>/comments/<int:comment_pk>',
"description": "show,update and delete comment from an especific post",
"methods": "get,put,delete",
},
{
"path" :'profile-activity/<int:pk>',
"description": "show activity from an especific profile",
"methods": "get",
},
{
"path" :'endpoints',
"description": "show all endpoints in this application",
"methods": "get",
},
]
