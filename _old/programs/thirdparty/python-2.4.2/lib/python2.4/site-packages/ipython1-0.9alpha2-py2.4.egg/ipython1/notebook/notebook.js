/********    mouseover menus    ********/




/*getParam from cryer.co.uk script8*/
getParam = function(name){
    var start=location.search.indexOf("?"+name+"=");
    if (start<0) start=location.search.indexOf("&"+name+"=");
    if (start<0) return null;
    start += name.length+2;
    var end=location.search.indexOf("&",start)-1;
    if (end<0) end=location.search.length;
    var result=location.search.substring(start,end);
    var result="";
    for(var i=start;i<=end;i++) {
        var c=location.search.charAt(i);
        result=result+(c=="+"?" ":c);
    }
    return unescape(result);
};

// globals
var gapID = 0;
var selectedCell = "";
var user = {};
var userlist = {};
var activeNotebook = null;
var pending = [];

/*********************** load/unload functions ********************/
connect = function(){
    var username = getParam("username");
    if (username == null){
    	username = prompt("username?", "");
    }
    var email = getParam("email")
    if (email == null){
    	email = prompt("email?", "");
    }
    selectedCell = "";
    gapID = 0;
    activeNotebook = null;
    pending = [];
    user = {};
    userlist = {};
    var d = doSimpleXMLHttpRequest("/connectUser", {email:email, username:username});
    d.addCallback(setUser);
    d.addCallback(getUserList);
};
disconnect = function(){
/*    alert("disconnecting");*/
    return doSimpleXMLHttpRequest("/disconnectUser", {userID:user.userID}); 
};
addLoadEvent(connect);

setUser = function(req){
    user = evalJSONRequest(req);
    if (!user.username){//try again
        alert("Connect User Failed");
    	var username = prompt("username?", "");
    	var email = prompt("email?", "");
        var d = doSimpleXMLHttpRequest("/connectUser", {email:email, username:username});
        d.addCallback(setUser);
        return d
    }else{
        var head = document.getElementById("header");
        head.innerHTML = "IPythonNotebook  " + user.username + ":" + user.email;
        return refreshNBTable();
    }
};
getUserList = function(){
    var d = doSimpleXMLHttpRequest("/getUsers");
    d.addCallback(_getUserList);
    return d;
};
_getUserList = function(req){
/*    return;*/
    userList = evalJSONRequest(req).list;
/*    return;*/
    var data = {};
    data.columns = ["username", "email", "userID"];
    data.rows = [];
    for (var i=0; i<userList.length; i++){
        var u = userList[i];
        var row = [];
        row.push(u.username);
        row.push(u.email);
        row.push(u.userID);
        data.rows.push(row);
    }
    sortableManager2.initWithData(data);
}

/*********************** sidebar functions ********************/
refreshNBTable = function(){
    var d = doSimpleXMLHttpRequest("/getNotebooks", {userID:user.userID});
    d.addCallback(setupNBTable);
    d.addCallback(getUserList);
    return d;
}
setupNBTable = function(req){
    var books = evalJSONRequest(req).list;
    var data = {};
    data.columns = ["title", "created", "modified", "permission", "notebookID"];
    data.rows = new Array;
    for (var i=0; i<books.length; i++) {
        var book = books[i];
        var row = [];
        book = setPermission(book);
        row.push(book.title);
        row.push(book.dateCreated);
        row.push(book.dateModified);
        row.push(book.permission);
        row.push(book.notebookID);
        data.rows.push(row);
    }
    sortableManager.initWithData(data);
};
addNotebook = function(){
    var title = prompt("Title", "title");
    var d = doSimpleXMLHttpRequest("/addNotebook", {userID:user.userID,title:title});
    d.addCallback(refreshNBTable);
    return d;
};
setPermission = function(book){
    if (book.userID == user.userID){
        book.permission = "own";
    }else{
        for (var i=0; i<book.writers.length; i++){
            if (book.writers[i] == user.userID){
                book.permission = "write";
                break;
            }
        }
        if (!book.permission){
            for (var i=0; i<book.readers.length; i++){
                if (book.readers[i] == user.userID){
                    book.permission = "read";
                    break;
                }
            }
        }
        if (!book.permission){
            alert("Permission setting error");
        }
    }
    return book;
};
setActiveNotebook = function(nbID){
    if (activeNotebook){
        closeNotebook();
    }
    var d = doSimpleXMLHttpRequest("/getNotebooks", {userID:user.userID, notebookID:nbID});
    d.addCallback(_setActiveNotebook);
    return d;
};
_setActiveNotebook = function(req){
    activeNotebook = evalJSONRequest(req).list[0];
    activeNotebook = setPermission(activeNotebook);
    if (!activeNotebook){
        alert(req.responseText);
    }else{
        var nbtd = getElementsByTagAndClassName("td", "notebook")[0];
        nbtd.innerHTML = "";
        nbtd.appendChild(permissionTable());
        nbtd.appendChild(nodeTableFromJSON(activeNotebook.root));
    }
};

/**** utility functions ******/
strip = function(s){
    while (s.length > 0 && s[0] == " "){
        s = s.substring(1);
    }
    while (s.length > 0 && s[s.length-1] == " "){
        s = s.substring(0,s.length-2);
    }
    return s;
};
getList = function(table, klass){
    var spanlist = getElementsByTagAndClassName("SPAN", klass);
    var readerlist = [];
    var i;
    var span;
    for (i=0;i<spanlist.length;i++){
        span = spanlist[i];
        if (getMyTable(span) == table){
            readerlist.push(span.innerHTML);
        }
    }
    return readerlist;
};
alertNode = function(node){
    var s = "id:"+node.nodeID+"\n";
    s += "nodeType:"+node.nodeType+"\n";
    alert(s);
};
getMyTable = function(element){
    while ((element.tagName != "TABLE") && element.tagName != "BODY"){
        element = element.parentNode;
    }
    return element;
};
getMySection = function(element){
    element = element.parentNode; // ensure that I don't get me back
    while ((element.tagName != "TABLE" || element.className != "section") && element.tagName != "BODY"){
        element = element.parentNode;
    }
    return element;
};
getMyChildren = function(section){
    return section.childNodes[section.childNodes.length-1].cells[0];
};
getUserByKey = function(key, value){
    for (var i=0;i<userList.length;i++){
        var u = userList[i];
        if (u[key] == value){
            return u;
        }
    }
}
isPending = function(nodeID){
    for (var i=0; i<pending.length; i++){
        if (nodeID == pending[i]){
            return true;
        }
    }
    return false;
};
isin = function(element, array){
    var i;
    for (i=0;i<array.length;i++){
        if (element == array[i]){
            return true;
        }
    }
    return false;
};

resizeTextArea = function(textarea,e){
        // this also captures Shift+Enter to execute
        var numRows = textarea.value.split("\n").length;
        var td = textarea.parentNode; // td
        if (e && e.keyCode == 13 && !(e.shifKey && td.className == "inContent")){
            textarea.style.height = (numRows+1 || 1).toString()+".2em";
        }else{
            textarea.style.height = (numRows || 1).toString()+".2em";
        }
        if (td.className == "inContent"){
            if (e && e.shiftKey && e.keyCode == 13){//shift-enter
                var d = updateTextArea(textarea, true);
                var t = getMyTable(textarea);
                pending.push(t.node.nodeID);
                textarea.disabled = true;
                if (!d){
                    execute(t.node.nodeID).addCallback(refreshNotebook);
                }else{
                    d.addCallback(function(){
                        execute(t.node.nodeID).addCallback(refreshNotebook);
                    });
                }
            }else{
                //proper action tbd
            }
        }
};
toggleCollapse = function(collapseObj){
    var t = getMyTable(collapseObj);
    for (var i=1; i<t.childNodes.length; i++){
        var row = t.childNodes[i];
        if (row.style.display == "none"){
            row.style.display = "";
        }else{
            row.style.display = "none";
        }
    }
};

/*********************** control functions ********************/
refreshNotebook = function(){
    if (!activeNotebook){
        alert("No Active Notebook!");
        return;
    }
    var d = getUserList();
    d.addCallback(function(){
        return doSimpleXMLHttpRequest("/getNotebooks", {userID:user.userID, notebookID:activeNotebook.notebookID});
    });
    d.addCallback(_setActiveNotebook);
    return d;
};
dropNotebook = function(){
    if (!activeNotebook){
        alert("No Active Notebook");
    }else{
        var d = doSimpleXMLHttpRequest("/dropNotebook",{userID:user.userID, notebookID:activeNotebook.notebookID});
        d.addCallback(refreshNBTable)
        activeNotebook = null;
        var nbtd = getElementsByTagAndClassName("td", "notebook")[0];
        nbtd.innerHTML = "";
    }
};
closeNotebook = function(){
    if (!activeNotebook){
        alert("No Active Notebook");
    }else{
        activeNotebook = null;
        var nbtd = getElementsByTagAndClassName("td", "notebook")[0];
        nbtd.innerHTML = "";
    }
};
dumpNotebook = function(){
    if (!activeNotebook){
        alert("No Active Notebook");
    }else{
        var loc = document.location;
        if (loc.search.indexOf("?") > -1){
            loc = loc.href.substring(0,loc.search.indexOf("?"));
        }
        var qs = queryString({userID:user.userID, notebookID:activeNotebook.notebookID});
        window.open(loc+"notebook.xml?"+qs);
    }
};

/*********************** main notebook functions ********************/
/** permissions section **/
permissionTable = function(){
    var t = document.createElement("table");
    t.className = "permission";
    var tr = document.createElement("tr");
    var td = document.createElement("td");
    if (activeNotebook.permission != "own"){
        td.className = "owner";
        td.innerHTML = "Owner:&nbsp;"
        var span = document.createElement("span");
        span.className = "owner";
        span.innerHTML = getUserByKey("userID",activeNotebook.userID).username;
        td.appendChild(span);
        tr.appendChild(td);
        td = document.createElement("td");
    }
    td.className = "readers";
    td.innerHTML = "Readers: ";
    for (var i=0;i<activeNotebook.readers.length;i++){
        span = document.createElement("span");
        span.className = "Reader";
        if (activeNotebook.permission == "own"){
            span.setAttribute("onclick", "dropUser(this);");
        }
        span.innerHTML = getUserByKey("userID",activeNotebook.readers[i]).username;
        td.appendChild(span);
        td.innerHTML += ", ";
    }
    if (activeNotebook.permission == "own"){
        ta = document.createElement("textarea");
        ta.className = "reader";
        ta.value = "add reader";
        ta.onfocus = function(){this.value = "";};
        ta.setAttribute("onblur", "addMembers(this);");
        ta.setAttribute("onkeypress", "maybeAddMembers(this, event);");
        td.appendChild(ta);
    }
    tr.appendChild(td);
    td = document.createElement("td");
    td.className = "writers";
    td.innerHTML = "Writers: ";
    for (var i=0;i<activeNotebook.writers.length;i++){
        span = document.createElement("span");
        span.className = "Writer";
        if (activeNotebook.permission == "own"){
            span.setAttribute("onclick", "dropUser(this);");
        }
        span.innerHTML = getUserByKey("userID",activeNotebook.writers[i]).username;
        td.appendChild(span);
        td.innerHTML += ", ";
    }
    if (activeNotebook.permission == "own"){
        ta = document.createElement("textarea");
        ta.className = "writer";
        ta.value = "add writer";
        ta.onfocus = function(){this.value = "";};
        ta.setAttribute("onblur", "addMembers(this);");
        ta.setAttribute("onkeypress", "maybeAddMembers(this, event);");
        td.appendChild(ta);
    }
    tr.appendChild(td);
    t.appendChild(tr);
    return t;
}
maybeAddMembers = function(textarea, event){
    if (event.keyCode == 13){
        addMembers(textarea);
    }
};
addMembers = function(textarea){
    var klass = textarea.className;
    var t = getMyTable(textarea);
    var args = {};
    args.userID = user.userID;
    args.notebookID = activeNotebook.notebookID;
    var l = textarea.value.replace(/\n/g, "").split(",");
    textarea.value = "";
    if (l.length == 0){
        return;
    }
    args[klass] = [];
    var users = getList(t, klass);
    var i;
    var u;
    var uname;
    for (i=0; i<l.length;i++){
        uname = strip(l[i]);
        u = getUserByKey("username", uname);
        if (u && !isin(uname, users) && !isin(u.userID, args[klass])){
            args[klass].push(u.userID);
        }
    }
    if (args[klass].length <= 0){
        return;
    }
    var d = doSimpleXMLHttpRequest("/add"+klass[0].toUpperCase()+klass.substring(1), args);
    d.addCallback(refreshNotebook);
    return d;
};
dropUser = function(span){
    var klass = span.className;
    var args = {};
    args.userID = user.userID;
    args.notebookID = activeNotebook.notebookID;
    span.parentNode.removeChild(span);
    args[klass] = getUserByKey("username", span.innerHTML).userID;
    var d = doSimpleXMLHttpRequest("/drop"+klass[0].toUpperCase()+klass.substring(1), args);
    d.addCallback(refreshNotebook);
};

/** main draw functions **/
gapTable = function(index){
    var t = document.createElement("table");
    t.className = "gap";
    t.id = index;
    //control
    var tr = document.createElement("tr");
    var td = document.createElement("td");
    td.className = "gap";
    td.innerHTML = "Insert:&nbsp;";
    span = document.createElement("span");
    span.className = "controlLink";
    span.onclick = function(){addSection(t);};
    span.innerHTML = "Section";
    td.appendChild(span);
    span = document.createElement("span");
    span.innerHTML = "&nbsp;&nbsp;|&nbsp;&nbsp;";
    td.appendChild(span);
    span = document.createElement("span");
    span.className = "controlLink";
    span.innerHTML = "IOCell";
    span.onclick = function(){addCell(t, "InputCell");};
    td.appendChild(span);
    span = document.createElement("span");
    span.innerHTML = "&nbsp;&nbsp;|&nbsp;&nbsp;";
    td.appendChild(span);
    span = document.createElement("span");
    span.className = "controlLink";
    span.innerHTML = "TextCell";
    span.onclick = function(){addCell(t, "TextCell");};
    td.appendChild(span);
    tr.appendChild(td);
    t.appendChild(tr);
    
    return t;
};
nodeTableFromJSON = function(node){
    var t = document.createElement("table");
    t.className = node.nodeType;
    t.node = node;
    t.setAttribute("id", node.nodeID);
    
    //header
    var tr = document.createElement("tr");
    tr.className = "nodeHead";
    var td = document.createElement("td");
    if (node.nodeType == "section"){
        td.className = "sectionTitle";
        if (activeNotebook.permission == "own" || activeNotebook.permission == "write"){
            td.setAttribute("onclick","updateTitle(this);");
        }
        td.innerHTML = node.title;
    }else{
        td.className = "cellTitle";
    }
    tr.appendChild(td);
    td = document.createElement("td");
    td.className = "nodeHead";
    td.innerHTML = " Modified:";
    var span = document.createElement("span");
    span.className = "date";
    span.innerHTML = node.dateModified;
    td.appendChild(span);
    td.innerHTML += " Created:";
    span = document.createElement("span");
    span.className = "date";
    span.innerHTML = node.dateCreated;
    td.appendChild(span);
    td.innerHTML += " nodeID:";
    span = document.createElement("span");
    span.className = "nodeID";
    span.innerHTML = node.nodeID.toString();
    td.appendChild(span);
    tr.appendChild(td);
    td = document.createElement("td");
    td.rowSpan = 6;
    td.className = "collapse";
    td.setAttribute("onclick", "toggleCollapse(this);");
    tr.appendChild(td);
    t.appendChild(tr);
    //control
    if (activeNotebook.permission == "own" || activeNotebook.permission == "write"){
        tr = document.createElement("tr");
        td = document.createElement("td");
        td.setAttribute("colspan", 2);
        td.className = "nodeActions";
        span = document.createElement("span");
        span.className = "controlLink";
        span.onclick = function(){moveNode(node.nodeID);};
        span.innerHTML = "move";
        td.appendChild(span);
        span = document.createElement("span");
        span.innerHTML = "&nbsp;&nbsp;|&nbsp;&nbsp;";
        td.appendChild(span);
        span = document.createElement("span");
        span.className = "controlLink";
        span.innerHTML = "drop";
        span.onclick = function(){dropNode(node.nodeID);};
        td.appendChild(span);
//        span = document.createElement("span");
//        span.innerHTML = "&nbsp;&nbsp;|&nbsp;&nbsp;";
//        td.appendChild(span);
//        span = document.createElement("span");
//        span.className = "controlLink";
//        span.innerHTML = "save";
//        span.onclick = function(){saveNode(node.nodeID);};
//        td.appendChild(span);
        tr.appendChild(td);
        t.appendChild(tr);
    }
    tr = document.createElement("tr");
    td = document.createElement("td");
    td.className = "tag";
    td.setAttribute("colspan", 2);
/*    td.innerHTML = "tags:"*/
    for (var i=0;i<node.tags.length;i++){
        span = document.createElement("span");
        span.className = "tag";
        if (activeNotebook.permission == "own" || activeNotebook.permission == "write"){
            span.setAttribute("onclick", "dropTag(this);");
        }
        span.innerHTML = node.tags[i];
        td.appendChild(span);
        td.innerHTML += ", ";
    }
    if (activeNotebook.permission == "own" || activeNotebook.permission == "write"){
        ta = document.createElement("textarea");
        ta.className = "tag";
        ta.value = "tag";
        ta.onfocus = function(){this.value = "";};
        ta.setAttribute("onblur", "addTags(this, event);");
        ta.setAttribute("onkeypress", "maybeAddTags(this, event);");
        td.appendChild(ta);
    }
    tr.appendChild(td);
    t.appendChild(tr);

    tr = document.createElement("tr");
    td = document.createElement("td");
    td.setAttribute("colspan", 2);
    td.className = "comment";
    var ta = document.createElement("textarea");
    ta.className = "comment";
    ta.setAttribute("onblur","updateTextArea(this,event);");
    ta.setAttribute("onkeypress", "resizeTextArea(this, event);");
    if (node.comment.length < 1){
        ta.value = "comments";
        ta.onfocus = function(){
            this.value = "";
            this.onfocus = null;
            };
    }else{
        ta.value = node.comment;
    }
    if (!activeNotebook.permission || activeNotebook.permission == "read"){
        ta.disabled = true;
    }
    td.appendChild(ta);
    tr.appendChild(td);
    t.appendChild(tr);
    resizeTextArea(ta,null);
    
    if (t.className == "section"){
        tr = document.createElement("tr");
        td = document.createElement("td");
        td.setAttribute("colspan", 2);
        td.className = "children";
        if (activeNotebook.permission == "own" || activeNotebook.permission == "write"){
            td.appendChild(gapTable(node.notebookID, 0));
        }
        for (var i=0; i<node.children.length; i++){
            td.appendChild(nodeTableFromJSON(node.children[i]));
            if (activeNotebook.permission == "own" || activeNotebook.permission == "write"){
                td.appendChild(gapTable(node.notebookID, i+1));
            }
        };
        tr.appendChild(td);
        t.appendChild(tr);
        
    }else if (t.className == "inputCell"){
        tr = document.createElement("tr");
        td = document.createElement("td");
        td.className = "input";
        td.setAttribute("colspan", 2);
        var div = document.createElement("div");
        div.className = "inLabel";
        div.innerHTML = "In&nbsp;&nbsp;:";
        td.appendChild(div);
        div = document.createElement("div");
        div.className = "inContent";
        ta = document.createElement("textarea");
        ta.setAttribute("onblur","updateTextArea(this,event);");
        ta.setAttribute("onkeypress", "resizeTextArea(this, event);");
        ta.className = "input";
        ta.value = node.input;
        if (!activeNotebook.permission || activeNotebook.permission == "read"){
            ta.disabled = true;
        }
        if (isPending(node.nodeID)){
            ta.disabled = true;
        }
        div.appendChild(ta);
        td.appendChild(div);
        tr.appendChild(td);
        t.appendChild(tr);
        resizeTextArea(ta,null);
        
        tr = document.createElement("tr");
        td.className = "output";
        td.setAttribute("colspan", 2);
        var ot = document.createElement("table");
        ot.className = "output"
        var otr = document.createElement("tr");
        var otd = document.createElement("td");
/*        div = document.createElement("div");*/
        otd.className = "outLabel";
        otd.innerHTML = "Out&nbsp;:";
        otr.appendChild(otd);
        otd = document.createElement("td");
        otd.className = "outContent";
        div = document.createElement("div");
        div.className = "outContent";
        if (node.output.length < 1 || isPending(node.nodeID)){
            div.innerHTML = "&nbsp;";
        }else{
            div.innerHTML = node.output.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/\n/g,"<br>\n");
        }
        otd.appendChild(div);
        otr.appendChild(otd);
        ot.appendChild(otr);
        td.appendChild(ot);
        tr.appendChild(td);
        t.appendChild(tr);
        
    }else if (t.className == "textCell"){
        tr = document.createElement("tr");
        td = document.createElement("td");
        td.setAttribute("colspan", 2);
        ta = document.createElement("textarea");
        ta.className = "format";
        ta.setAttribute("onblur","updateTextArea(this,event);");
        ta.setAttribute("onkeypress", "resizeTextArea(this, event);");
        if (!node.format || node.format.length < 1){
            ta.value = "format";
            ta.onfocus = function(){
                this.value = "";
                this.onfocus = null;
                };
        }else{
            ta.value = node.format;
        }
        if (!activeNotebook.permission || activeNotebook.permission == "read"){
            ta.disabled = true;
        }
        td.appendChild(ta);
        tr.appendChild(td);
        t.appendChild(tr);
        resizeTextArea(ta,null);
        
        tr = document.createElement("tr");
        td = document.createElement("td");
        td.setAttribute("colspan", 2);
        ta = document.createElement("textarea");
        ta.className = "textData";
        ta.setAttribute("onblur","updateTextArea(this,event);");
        ta.setAttribute("onkeypress", "resizeTextArea(this, event);");
        if (node.textData.length < 1){
            ta.value = "Text Data";
            ta.onfocus = function(){
                this.value = "";
                this.onfocus = null;
                };
        }else{
            ta.value = node.textData;
        }
        if (!activeNotebook.permission || activeNotebook.permission == "read"){
            ta.disabled = true;
        }
        td.appendChild(ta);
        tr.appendChild(td);
        t.appendChild(tr);
        resizeTextArea(ta,null);
    }
    return t;
};
updateTitle = function(titleTD){
    var t = getMyTable(titleTD);
    newtitle = prompt("New Title", t.node.title)
    if (t.node.title == newtitle){
        return;
    }
    args = {};
    args.userID = user.userID;
    args.nodeID = t.node.nodeID;
    args["title"]= newtitle;
    var d = doSimpleXMLHttpRequest("/editNode", args);
    d.addCallback(_updateNode, t);
};
updateTextArea = function(textarea){
    var t = getMyTable(textarea);
    if (t.node[textarea.className] == textarea.value){
        //no change
        return;
    }
    args = {};
    args.userID = user.userID;
    args.nodeID = t.node.nodeID;
    args[textarea.className]= textarea.value;
    var d = doSimpleXMLHttpRequest("/editNode", args);
    d.addCallback(_updateNode, t);
    return d;
};
_updateNode = function(t,req){
    var node = evalJSONRequest(req);
    var newt = nodeTableFromJSON(node);
    swapDOM(t, newt);
};

/********** tag functions    ***********/
getTags = function(table){
    var spanlist = getElementsByTagAndClassName("SPAN", "tag");
    var taglist = [];
    var i;
    var span;
    for (i=0;i<spanlist.length;i++){
        span = spanlist[i];
        if (getMyTable(span) == table){
            taglist.push(span.innerHTML);
        }
    }
    return taglist;
};
maybeAddTags = function(textarea, event){//check for <Enter>
    if (event.keyCode == 13){
        addTags(textarea);
    }
};
addTags = function(textarea){
    var t = getMyTable(textarea);
    var args = {};
    args.userID = user.userID;
    args.nodeID = t.node.nodeID;
    var l = textarea.value.replace(/\n/g, "").split(",");
    textarea.value = "";
    if (l.length == 0){
        return;
    }
    var taglist = getTags(t);
    args.tags = [];
    var len = args.tags.length;
    var i;
    var tag;
    for (i=0; i<l.length;i++){
        tag = strip(l[i]);
        if (tag != "" && !isin(tag, args.tags)){
            args.tags.push(tag);
        }
    }
    if (args.tags.length <= len){
        return;
    }
    var d = doSimpleXMLHttpRequest("/addTag", args);
    d.addCallback(_updateNode, t);
};
dropTag = function(span){
    var t = getMyTable(span);
    var args = {};
    args.userID = user.userID;
    args.nodeID = t.node.nodeID;
    span.parentNode.removeChild(span);
    args.tags = span.innerHTML;
    var d = doSimpleXMLHttpRequest("/dropTag", args);
    d.addCallback(_updateNode, t);
}
/********** node functions    ***********/

addSection = function(gapt){
    var args = {};
    args.userID = user.userID;
    var t = getMyTable(gapt);
    var parentT = getMySection(t);
    var childrenTD = getMyChildren(parentT);
    args.parentID = parentT.node.nodeID;
    for (var i=0;i<childrenTD.childNodes.length;i++){
        if (childrenTD.childNodes[i] == t){
            args.index = i/2;
            break;
        }
    }
    args.title = prompt("Title");
    args.nodeType = "Section";
    var d = doSimpleXMLHttpRequest("/addNode",args);
    d.addCallback(refreshNotebook);
};
addCell = function(gapt, nodeType){
    var args = {};
    args.userID = user.userID;
    var t = getMyTable(gapt);
    var parentT = getMySection(t);
    var childrenTD = getMyChildren(parentT);
    args.parentID = parentT.node.nodeID;
    for (var i=0;i<childrenTD.childNodes.length;i++){
        if (childrenTD.childNodes[i] == t){
            args.index = i/2;
            break;
        }
    }
    args.nodeType = nodeType;
    var d = doSimpleXMLHttpRequest("/addNode",args);
    d.addCallback(refreshNotebook);
};
dropNode = function(nodeID){
    var args = {};
    args.userID = user.userID;
    args.nodeID = nodeID;
    var d = doSimpleXMLHttpRequest("/dropNode",args);
    d.addCallback(refreshNotebook);
};
moveNode = function(nodeID){
    var args = {};
    args.userID = user.userID;
    args.nodeID = nodeID;
    args.parentID = prompt("new parent?");
    args.index = prompt("new Location?");
    var d = doSimpleXMLHttpRequest("/moveNode",args);
    d.addCallback(refreshNotebook);
};
execute = function(nodeID){
    var args = {};
    args.userID = user.userID;
    args.nodeID = nodeID;
    var d = doSimpleXMLHttpRequest("/execute",args);
    d.addCallback(_execute, nodeID);
    d.addCallback(refreshNotebook);
    return d;
};
_execute = function(nodeID, result){
    for(var i=0; i<pending.length;i++){
        if(nodeID == pending[i]){
            pending = pending.slice(0,i).concat(pending.slice(i+1));
        }
    }
    return result;
};
