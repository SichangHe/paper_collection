# Automated Transformation Of Template-Based Web Applications Into Single-Page Applications

Jaewon Oh*+, Woo Hyun Ahn§, Seungho Jeong*, Jinsoo Lim*, Taegong Kim\# 
* School of Computer Science and Information Engineering, The Catholic University of Korea, Bucheon, Korea 
+ jwoh@catholic.ac.kr c Department of Computer Science, Kwangwoon University, Seoul, Korea, whahn@kw.ac.kr 
\# Department of Computer Engineering, Inje University, Gyeongnam, Korea, sun@inje.ac.kr Abstract—In a template-based web application (TWA), a template is used as a common structure or layout to dynamically generate web pages. The consistent structure helps users easily obtain information. However, TWAs still have an interaction problem: whenever a user clicks a hyperlink or submits a form, a new page is loaded. Therefore, we need to reduce communication between a browser and a server by avoiding loading the same template twice. This paper proposes a technique of transforming a Java-based TWA into a single-page application (SPA) with partial page refreshes. An Eclipse plugin is also presented for automatic reengineering of TWAs. Our technique is applied to typical TWAs and discussed with respect to quality attributes such as performance, bookmarkability, and backward navigation. 

Keywords-web template; single-page application; AJAX; 
reengineering 

## I. Introduction

A template-based web application (TWA) uses a template to dynamically generate web pages. The template is a common layout or structure that is shared by the pages of the application. A template is an HTML file containing placeholders that can be filled with results of simple actions 
[13].1 Fig. 1 shows a typical TWA written in Java language. 

The pages of the TWA comprise a template (a common part) 
and contents (a page-specific part) that result from executing the <jsp:include> standard action of line 19. Placeholders of a template are usually filled in with <jsp:include> standard actions or include directives in Java-based development. To condense our explanation, in this paper we assume that TWAs use the standard actions, but our transformation approach can also be applied to TWAs with the include directives. 

Traditional web applications including TWAs interact with users using a multi-page application (MPA) model. In the model, client browsers download and render a new page each time users click a hyperlink or submit a form. In contrast, a single-page application (SPA) is a web application that processes a request from a user without refreshing a full page. The partial page refresh can be achieved by using AJAX (Asynchronous JavaScript and 
 § Corresponding author XML) [5], which is a set of web development technologies to make web applications more interactive and responsive, similar to desktop applications. 

Currently, the TWA development is a popular approach due to two advantages. First, it can reduce the amount of redundant code and improve development productivity or modularity, thus increasing the level of maintainability and reuse of applications. Second, users can easily obtain information guided by a consistent structure of the template [8]. 

TWAs, however, have the same interaction problem as traditional web applications. The problem is that a new page is loaded whenever a user clicks a hyperlink or submits a form. For example, when a user clicks on a *write* menu (line 15 of Fig. 1(a)) to post a book review, a browser redundantly downloads and displays the left menus and the company description at the top and bottom of the page. 

The interaction problem has been solved in the previous researches [11, 19, 18] in which MPAs are migrated to SPAs. The researches mainly focus on UI redesign without modifying the server code (written in ASP, JSP, PHP, etc.). 

However, efficient partial page refreshes require a server code to be analyzed and transformed into a code that sends only the changed data to browsers in response to a request. Such a transformation is proposed in some studies [22, 1, 21], but they only consider forms or web pages displaying a list of data (e.g., search results), and are thus insufficient for application to general TWAs. 

This paper proposes a reengineering technique to transform the multi-page structure of legacy Java-based TWAs into SPAs with partial page refreshes. The scheme reduces communication between a browser and a server by avoiding loading the same template twice and avoiding refreshing pages on a form submission. Such a reduction is achieved by refactoring hyperlinks and forms in HTML code to elements with the AJAX-enabled event handlers. In addition, JSP/Servlet (server-side) and HTML/JavaScript 
(client-side) code is refactored to prevent web servers from sending data unnecessary for the partial update. Our policy has the additional advantage of reducing interaction among server components such as JSPs and Servlets by bypassing the template. Moreover, our policy for reengineering is to produce applications that comply with web standards and that do not use any libraries and plugins. An Eclipse plugin is also presented for the automatic reengineering of TWAs. An earlier version of this paper appeared in [12]. 

To validate our proposed technique, in this paper we compare our technique with a PJAX [16] based approach to transforming a TWA into an SPA. The PJAX is a jQuerybased library which provides functionality for the partial page update via AJAX. When the PJAX is applied to transform a TWA into an SPA, the resulting SPA is used without a full page reload if a browser supports the HTML5 history API [14]. Otherwise, the SPA is used with a full page refresh similarly to the original TWA. 

The paper is organized as follows. Research problems and our approach are described first, followed by information on the reengineering technique to transform Java-based TWAs into SPAs. An Eclipse plugin is then proposed for the automatic reengineering of TWAs. In the next section, the performance of our transformation approach and a PJAX-based approach is then evaluated and analyzed. 

In the remainder of the paper, we first discuss how well our approach solves the research problems. The related work is then introduced. Finally, the paper is concluded with a short summary of our reengineering approach. 

## Ii. Problem And Approach

In this section, we discuss the redundancy problem with TWAs. The problem is illustrated in a typical TWA 
application, online book publisher, in which users obtain the information on books and then write and/or read reviews on books. The application is built on an MVC (Model-ViewController) [15, 20], which is a popular architecture pattern in J2EE applications. The application is a modified version of an application described in [9]. 

Figure 2 shows a scenario of how the application processes the review posting of a user on books. In the scenario, collaborating objects are as follows. The ReviewBean JavaBean object is a model that processes read/write transactions for reviews in a database. The ReviewForm JSP object is a view that obtains user input delivered to the controller *ReviewCtrl*. Taking the user input, the *ReviewCtrl* Servlet object is a controller that tells the model *ReviewBean* to update itself and generate some data 
(e.g., information between write success and failure) 
available to the view *ReviewRslt*. The *ReviewRslt* JSP object is another view which displays the result of a review write transaction. The *Template* JSP object is a view which provides a common layout to all the web pages. 

The scenario for the TWA (Fig. 2(a)) is as follows: 
- Visit to an initial page (steps 1-3): a user opens an initial page of the application. A web browser sends an HTTP request for the view *Template* to a web server. The server locates and processes the Template, which generates a web page. Finally, the server sends the browser the web page as a response. 

- Download of a review form (steps 4-8): the user clicks a menu item in the initial page to write a review on a book. The browser sends an HTTP request for the *Template* to the server. The *Template* receives a URL of the *ReviewForm* as an input parameter. Next, the *Template* combines its response with a response from the *ReviewForm* and generates a web page. The server sends the page to the browser. 

- Submission of the review form (steps 9-16): when the user fills out and submits the review form, the browser sends a request for the controller ReviewCtrl. The *ReviewCtrl* receives the data typed in the form as input parameters. The *ReviewCtrl* tells the *ReviewBean* to store the data in a database. To show the result of the review write, the *ReviewCtrl* forwards the user request to the *Template*. The Template receives a URL of the view *ReviewRslt* as an input parameter. The *Template* then combines its response with a response from the *ReviewRslt* and generates a web page. The server sends the browser the web page as a response. 

An important problem is observed from analyzing the scenario of the TWA. A layout or view common to web pages is stored and managed in only one place, in the Template. Sharing the same template in web pages reduces code duplication, compared with traditional web applications that do not use templates. However, whenever a user clicks a hyperlink or submits a form, a new page including a response from a template is loaded. Such a loading of a template is an unnecessary and repeatable work, as seen in steps 8 and 16 of Fig. 2(a), thus causing the duplication problem from the runtime's perspective. 

The runtime duplication problem can be solved by removing two operations: the redundant template download and the display. 

- Redundant download: to eliminate the download 
(e.g., steps 5-8 of Fig. 2(a)), a browser should make a request for the changed data (step 5 of Fig. 2(b)) rather than the entire page. In addition, even when a browser makes a request for a controller (step 11 of Fig. 2(a) and step 10 of Fig. 2(b)), a server should reply with the changed data (steps 12-14 of Fig. 2(b)) rather than the entire page (steps 13-16 of Fig. 2(a)). 

- Redundant display: to avoid redisplaying the template, a browser should not make an HTTP 
request because the request requires the entire page to refresh. Additionally, a browser should update only a page-specific part. Steps 5-7 in Fig. 2(b) show such a request and its response for the *ReviewForm* and a partial page refresh with the response. 

Fig. 2(b) shows a new scenario of how an SPA resolves the duplication problem of the TWA. The scenario is functionally equivalent to the scenario of Fig. 2(a). To realize the scenario of the SPA, in section III we propose a novel approach to transforming legacy TWAs into SPAs. 

## Iii. Transformation Method

In this section, we describe our transformation approach to reengineering Java-based TWAs into single-page AJAX 
applications in detail. 

A. *Identification of Placeholder in Template* page is refactored to eliminate the page switching as follows: 

![2_image_0.png](2_image_0.png) Such a refactoring is achieved by removing an *href* attribute and registering an *onclick* event handler. 

(a) Flow of events in TWA 

![2_image_2.png](2_image_2.png)

(b) Flow of events in SPA 
Figure 2. Scenario for posting a book review 

1: <%@page contentType="text/html; charset=utf-8" %> 
2: <HTML> 
3: <HEAD> <TITLE> Web Dev Press</TITLE> </HEAD> 
4: <BODY> 
5: <FORM method=get action="BookSearch"> 
6: <INPUT type=text name=SEARCH> 
7: <INPUT type=submit value="Search"> 
8: </FORM> 
9: <TABLE border=1> 
10: <TR> 
11: <TD width=190 valign=top> 
12: <A HREF="Template.jsp?Body=Intro.html">About</A><BR>
13: <A HREF="BooksRead">Books</A><BR> 
14: Books review<BR> 
15: <A HREF="Template.jsp?Body=ReviewWrtie.jsp">Write</A><BR>
16: <A HREF="ReviewRead">Read</A><BR>
17: </TD> 
18: <TD valign=top width=650> 
19: <jsp:include page="${param.Body}" />
20: </TD> 
21: </TR> 
22: </TABLE> 23: <H5> @ 2012 Web Dev Press … <H5> 
24: </BODY> 
25:</HTML>

![2_image_1.png](2_image_1.png)

(b) Web page generated from Template.jsp when clicking on the *write* menu (line 15 of (a)) to write a review on a book Figure 1. Example of a template-based web application One of the objectives of our approach is to remove a full page refresh. In a template file, we first need to specify independently updatable elements (i.e., placeholders for page-specific contents). In a TWA, web pages are generated from the template by including contents specific to the pages. 

The region showing the result of the <jsp:include> action can be considered as an independently updatable element. 

A <jsp:include> action is enclosed by a new <span> or 
<div> element which represents a section in an HTML 
document. A unique value is assigned to an id attribute of the element as well. We can make a single-page UI, which only allows the <span> or <div> region to change while interacting with a user. An example of the transformation is shown in line 19 of Fig. 1(a) and line 19 of Fig. 3. Here, the 
<span> element with *id = "container"* is introduced. 

B. *Transformation of Hyperlink into AJAX Hyperlink* Hyperlinks connecting web pages need to be analyzed to remove the switching between the pages. These links are specified by <a> tags. A hyperlink going to another web Figs. 1 and 3 show an example of how a hyperlink is refactored. In Fig. 3, when a user clicks on a *write* menu (line 15) to post a book review, the *onclick* event handler doGetByAjax('ReviewWrtie.jsp') is executed to send an AJAX request to the view *'ReviewWrtie.jsp'*, from which the response is placed in the <span> element with *id =* 
"container". The look and feel of the resulting page is the same as in Fig. 1(b). 

In the refactoring, hyperlinks are classified into two categories, depending on whether or not a template address is directly used in a URL of a hyperlink. In one hyperlink, the href attribute includes a template address and an input parameter of the template, e.g., URLs used in line 15 of Fig. 

1(a) and step 5 of Fig. 2(a). The other hyperlink does not have a template address in its *href* attribute, e.g., URLs used in line 13 of Fig. 1(a) and step 11 of Fig. 2(a). Henceforth, the first category is referred to as a *hyperlink with a directly* referenced template, and the second category as a hyperlink with an indirectly referenced template. 

1) *Hyperlink with Indirectly Referenced Template* When a user makes a request for a page in a TWA based on the MVC, a browser usually sends the request to a controller, which executes its business logic and forwards the request to a template view to generate the page (refer to Fig. 4(a)). In this subsection, we describe how this dynamic structure of TWAs is transformed into a single-page architecture as shown in Fig. 4(b). 

Hyperlinks with an indirectly referenced template do not encompass a template address in their *href* attributes. One example of such a hyperlink connected to a controller is shown in line 1 of Fig. 5(a). The hyperlink is refactored as described in subsection III.B: an *href* attribute of the link is removed. Instead, an event handler is registered on the onclick event of the <a> element (step 1 of Fig. 4(b) and line 2 of Fig. 5(a)). 

In TWAs, clicking on a hyperlink in step 10 of Fig. 2(a) 
issues an HTTP request. To process the request, a web server executes some business logic and then prepares a new page using a template (e.g. step 13 of Fig. 2(a)). For the preparation, a controller uses a *RequestDispatcher* object acting as a wrapper for the template. The object generates a response with a consistent layout as shown in line 1-2 of Fig. 

5(b). 

In SPAs, a template should not be sent to a browser, to avoid the browser receiving unnecessary data from the server. Therefore, at the architecture level, the controller avoids using the template as shown in Fig. 4(b). At the code level, the template address in the parameter of the getRequestDispatcher() method is removed, as shown in Fig. 

5(b). Therefore, we can see that the interaction between web components is reduced by bypassing the template. 

2) *Hyperlink with Directly Referenced Template* When a page-specific part of a page is a static HTML 
file, a browser can send a request to a template, which receives a URL of the part as an input parameter. The template then generates a page consisting of its response and the response produced by including the parameter (refer to Fig. 6(a)). In this subsection, we describe how this dynamic structure of TWAs is transformed into a single-page architecture as shown in Fig. 6(b). 

In hyperlinks with directly referenced templates, the value format of the *href* attributes of these hyperlinks is as follows: *"templateAddress?includedPageAddress"*. Such a hyperlink is illustrated in line 1 of Fig. 7(a). It is refactored as described in subsection III.B. 

In SPAs, a template should not be sent to a browser twice. Therefore, our approach ensures that web pages do not include a response from a template at the architecture level, as shown in Fig. 6(b). At the code level, the template address in the *href* attribute is not used. For example, as can be seen in Fig. 7(a), the value *Intro.html* of the input parameter *Body* of the template is passed to the event handler *doGetByAjax()*. 

The input URL is then used in the method *open()* of the object *XMLHttpRequest* (line 3 of Fig. 7(b)) to specify the location of the desired resource. Therefore, we can see that the interaction between web components is reduced by bypassing the template. 

1~4: same as lines 1-4 of Fig. 1(a) 
5: <FORM id="Template0" onSubmit="doGetFormByAjax(this.id,'BookSearch'); return false;"> 
6: <INPUT type=text name=SEARCH> 
7: <INPUT type=submit value='Search'> 
8: </FORM> 
9~11: same as lines 9-11 of Fig. 1(a) 
12: <A onclick="doGetByAjax('Intro.html');">About</A><BR> 13: <A onclick="doGetByAjax('BooksRead');">Books</A><BR> 
14: same as line 14 of Fig. 1(a) 
15: <A onclick="doGetByAjax('ReviewWrtie.jsp');">Write</A><BR>
16: <A onclick="doGetByAjax('ReviewRead');">Read</A><BR>
17~18: same as lines 17-18 of Fig. 1(a) 
19: <span id="container"> <jsp:include page="${param.Body}" /> </span>
20-25: same as lines 20-25 of Fig. 1(a)
Figure 3. Example of a single-page application. TWA of Fig. 1 is transformed into this application 

![3_image_0.png](3_image_0.png)

(a) Structure of TWA based on MVC b) Structure of SPA 
Figure 4. Transforming architecture for reducing interaction among web components in the case of using hyperlinks with indirectly referenced templates 1: <A HREF="BooksRead">Books</A>
-

2: <A onclick="**doGetByAjax('BooksRead');**">Books</A> 
(a) View (written in HTML/JSP) which generates web pages 1: RequestDispatcher dispatcher = request.getRequestDispatcher("Template.jsp?Body=BooksReadView.jsp"); 2: dispatcher.forward(request, response);
- 
3: RequestDispatcher dispatcher = request.getRequestDispatcher("**BooksReadView.jsp**"); 4: dispatcher.**include**(request, response);
(b) Controller in Java Servlet Figure 5. Transforming hyperlinks with indirectly referenced templates 

![4_image_0.png](4_image_0.png)

(a) Structure of TWA based on MVC (b) Structure of SPA 
Figure 6. Transforming architecture for reducing interaction among web components in the case of using hyperlinks with directly referenced templates 1: < A HREF="Template.jsp?Body=Intro.html">About</A> 

![4_image_1.png](4_image_1.png)

2: <A onclick="**doGetByAjax('Intro.html');**">About</A> 

(a) HTML/JSP 

![4_image_2.png](4_image_2.png)

Figure 7. Transforming hyperlinks with directly referenced templates 

## C. Transformation Of Form Into Ajax Form

A form is an HTML element with input fields such as a text field, a radio button, and a menu that allows users to enter information. When the form is submitted, its data values are paired with their corresponding names, which are sent to a server together with the data values [17]. After the server processes the data, a browser receives and displays a new web page as a response from the server. 

The page refresh caused by the form submission is removed by refactoring a form as follows (a transformation example is shown in Fig. 8): 
- A unique value is assigned to an id attribute and an action attribute is removed (lines 1 and 5 of Fig. 

8(a)). Next, we register an AJAX-enabled function with the id and *action* value as input on an *onsubmit* event (line 5 of Fig. 8(a)). To stop a form being submitted, *"return false"* is appended to the end of the *onsubmit*. Therefore, when a user submits a form, an AJAX request is made and sent to a server by the function and then the *submit* event is canceled, and the page refresh does not occur. 

- The event handler (see Fig. 8(b)) works as follows. 

First it retrieves all the form data using a form id and packages the data into a string (line 2). Next, the handler makes up an AJAX request by appending the packaged form data to the end of the URL (line 3) and issues the request (line 4). 

- Here, our approach considers a *method* attribute of a form that determines how the form data are sent to a server. Two functions, *doGetFormByAjax()* and doPostFormByAjax(), are provided (lines 1-9 of Fig. 

8(b)) because there are two primary methods: GET and POST. A GET makes up a request by appending the packaged form data to the end of the URL (line 3) and sends the request to a web server, while a POST sends a request whose body includes the form data (line 21). To perform an AJAX request in a POST style, the function *doPostByAjax()* is added (lines 10-22), and a GET-style *doGetByAjax()*
was introduced in Fig. 7(b). 

A URL of the *action* attribute usually references a template indirectly because it locates a controller of the MVC pattern. In this case, form submission can be considered as a click on a hyperlink with an indirectly referenced template. The *action* attribute is considered as the href attribute of such a hyperlink. So, the transformation described in subsection II.B.1 is applied to the form (see lines 1 and 5 of Fig. 7(a)). On the other hand, if a URL of the action attribute references a template directly, the transformation described in subsection III.B.2 is applied. 

## D. Backward Navigation

Each time a user visits a new page, a browser's address bar changes into a new URL, which is pushed into a browser's history stack [14]. If the user clicks a back button, the pointer of the stack moves down the stack [4]. The address bar also changes into a URL of the repositioned pointer and a page with the address is loaded. This means that the browser maintains a history of URLs that a user has visited. 

Within the context of an AJAX application, clicking a back button has different results. When a user clicks an AJAX link, the state of the application changes without altering a URL in the address bar [4]. The history stack also does not change. Therefore, pressing a back button would not load a previous state of the application, but rather load a page which was visited before the application. This is because the browser does not maintain a history of the states that a user has entered during the interaction with an AJAX application. Such a behavior induces the user to fail to revisit previously visited states through forward and backward navigation. 

The problem on the back button is solved by applying the HTML5 history API to our reengineering approach. The API 
was introduced to manage the browser history via script [14]. 

The history API is provided by the following two interfaces: 
the *history.pushState()* function and the *popstate* event on the window object. The *history.pushState()* function pushes a new entry into the history stack and alters a URL in a browser's address bar without a full page reload. When the entry is visited through forward or backward navigation, the popstate event is fired [4]. Our SPA is equipped with the history API to support backward and forward navigation as follows: 
- When a browser receives an AJAX response, it calls a function registered on the *onreadystatechange* event of the *XMLHttpRequest* (e.g., lines 4-10 of Fig. 7(b)). This function inserts a downloaded HTML snippet into the current page using the innerHTML property (e.g., line 7 of Fig. 7(b)). 

Subsequently, the *history.pushState()* function is called to push the new state (i.e., the HTML snippet) 
into the history stack (see Fig. 9). 

- If a user presses the back button and the browser notices the stack entry has been manually pushed into the stack, the browser then fires a *popstate* event. A function registered on the event forces the browser to return the previous state popped out from the history stack to the SPA. The state is then inserted into the current page to restore the previous page (see Fig. 10). 

## E. Bookmarkability

Bookmarkability means that every URI references a unique resource and that every resource is pointed to by a URI [10]. Originally, an AJAX application changes its state without altering a URL in a browser's address bar. This implies that the states of the application are mapped to a single URL. Therefore, you cannot bookmark a specific state. In contrast, our SPA distinguishes one state from another by using the HTML5 history API as described in the previous subsection. However, a unique URL is not yet assigned to each state. Therefore, this section describes a one-to-one correspondence from application states to URLs to enable bookmarkability in our SPAs. 

When a new state is inserted into the history stack by using the *history.pushState()* function, a URL for the state is passed to the function as shown in line 2 of Fig. 9. The third parameter of the function denotes such a URL, which appears in the browser's address bar. Note that upon sending an AJAX request for a resource, the request URL uniquely identifies the resource within an SPA. In the paper, this fact is utilized to allocate unique URLs to application states as follows: *templateAddress?Body=AJAXRequestURL* where templateAddress, *Body*, and *AJAXRequestURL* represent a URL of a template, a parameter name for receiving a URL of a page-specific part, and a parameter value, respectively. 

For example, in Fig. 1(a), when clicking on a *write* menu 
(line 15) to post a book review, the AJAX request URL becomes *"ReviewWrtie.jsp"* (see line 15 of Fig. 3) according to the rule described in Figs. 6 and 7. The URL of the corresponding new state becomes 
"Template.jsp?Body=ReviewWrtie.jsp" according to the above rule. The constructed URL is identical to the URL used to send the same request in the TWA. Table I shows examples of such mapping between these request URLs. If an AJAX request is issued to a view, the resulting page's URL is the same as that of its original HTTP request in a TWA. If an AJAX request is issued to a controller, the resulting page's URL differs from that of its original HTTP 
request. This is because the original request's URL does not begin with the *templateAddress*. 

A bookmarked URL can be visited later. When this happens, our approach generates a page with a full page refresh as follows: first, a browser sends an HTTP request for the template to a web server. The template receives a URL of a page-specific part as an input parameter. When the part is generated by a controller, collaboration occurs among web components as shown in Fig. 11(a). Figure 11(b) shows the interaction among the components in the case where the part is provided by a view. In this process, a new entry is not pushed into the history stack by the function *pushState()*
because the browser automatically pushes a new entry into the stack. 

A page can be refreshed in the same way as above. In addition, forward and backward navigation is still possible because URLs are only added as input in the *pushState()* function. 

## Iv. Tool For Transformation Of Twa Into Spa

We have developed an Eclipse plugin to transform TWAs into SPAs (see Fig. 12). First, the plugin takes two inputs by using a wizard UI as shown in Fig. 12(a). One input is a project folder including a TWA to be transformed. The other is a template string whose format is as follows: 
templateAddress?Body=, where *templateAddress* denotes a URL of a template and *Body* represents an input parameter name for obtaining a URL of a page-specific part. 

Next, a refactoring engine runs with original files in the project folder and the template string in two steps. In step 1, code smells (i.e., code snippets to be transformed) are selected based on the conditions of the reengineering rules described in the previous section. Jericho HTML parser [6] is used in order to search HTML and JSP files for code smells. This is because both HTML and JSP tags are recognized and can be modified by the parser. We do not reuse any existing parsers for analysis of Java files. In step 2, code smells are modified according to the action of the selected rule. 

![5_image_0.png](5_image_0.png)

-

5: <FORM id="Template0" onSubmit="doGetFormByAjax(this.id,'BookSearch'); return false;">
6-8: same as lines 2-4 of original version
(a) HTML/JSP 
1: function doGetFormByAjax(formId, url) { 2: var paramList = packageFormData(formId); // all the form data values are retrieved using a formId, 

![5_image_1.png](5_image_1.png)

![5_image_3.png](5_image_3.png)

![5_image_4.png](5_image_4.png)

![5_image_6.png](5_image_6.png)

paired with their corresponding names, and then concatenated into a string paramList 3: var urlWithParam = url + "?" + paramList; 

![5_image_2.png](5_image_2.png)

![5_image_5.png](5_image_5.png) ![5_image_7.png](5_image_7.png)

![5_image_9.png](5_image_9.png)

Figure 8. Transforming traditional form 

![5_image_8.png](5_image_8.png)

Figure 9. JavaScript for pushing a new state in a browser history stack 1: window.onpopstate = popState; 2: function popState(event) { 
3: var **placeholder** = document.getElementById("**container**"); 
4: **placeholder.innerHTML = event.state.condition**; 
5: }
Figure 10. JavaScript for obtaining a previous state form a browser history stack

1: var **newState** = { **condition: xhr.responseText** }; 
2: history.pushState( **newState**, null, "Template.jsp" + "?Body=" + url );

| TWA                        | SPA                                      |                                        |
|----------------------------|------------------------------------------|----------------------------------------|
| Page request  AJAX request | Page request                             |                                        |
| URL                        | URL                                      | URL                                    |
| Controller BooksRead       | BooksRead                                | Template.jsp?Body                      |
| Pagespecific                            | = BooksRead                              |                                        |
| View                       | Template.jsp?Body =Intro.html Intro.html | Template.jsp?Body                      |
| part                       | =Intro.html                              |                                        |
| Request process            | Full page refresh                        | Partial page refresh Full page refresh |

![6_image_0.png](6_image_0.png)

(a) In the case where an AJAX 
request is issued to a controller 
(b) In the case where an AJAX 
request is issued to a view Figure 11. Transforming architecture for page refresh 

![6_image_1.png](6_image_1.png)

![6_image_2.png](6_image_2.png)

(b) UI for showing results of reengineering of TWA 
Figure 12. Tool for transformation of TWA into SPA 
When the refactoring engine finishes reengineering, a list of modified files is shown in a newly developed view (i.e., 
Change File View) of the Eclipse IDE. A file can be selected in the view and the differences between the file and its original file can be viewed using the Eclipse compare (as shown in Fig. 12(b)). 

## V. Experiment And Analysis

To validate the usefulness of our transformation approach, we perform an experiment on the typical TWA 
introduced in section II and its transformed SPA version. A 
PJAX-based approach is also compared with our transformation approach. 

The PJAX is an open source library that provides web applications with the functionality for the PJAX interaction, which enables the partial page refresh and the backward navigation. The library adjusts its communication behavior, depending on the state of web browsers, web servers, and the network. If a browser running a PJAX-based application supports the HTML5 history API, the PJAX interaction is used between servers and browsers. Otherwise, the application uses the normal HTTP interaction. In addition, when the PJAX request processing time exceeds a configurable parameter *timeout* threshold (e.g., due to complex processing on servers), the request falls back to a new HTTP request. A TWA is transformed into an SPA by using the PJAX library as follows: 
- Server-side: the *X-PJAX* HTTP request header is provided in the library to differentiate PJAX requests from normal *XMLHttpRequest* and HTTP requests [16]. If a request is a PJAX request (i.e., the header is set to true), the SPA skips the template code and generates the response with only a page-specific part 
(lines 5-11 of Fig. 13(a)). Otherwise, the SPA runs in the same way as the original TWA (lines 13-38 of Fig. 13(a)). 

- Client-side: PJAX requests are issued when a user clicks on hyperlinks (see line 40 of Fig. 13(b)). During the request processing, the PJAX enables the SPA to obtain a page-specific part via AJAX, which is inserted in the placeholder (i.e., the <span>
element with *id = "pjax-container"*) of the template. 

The PJAX-based SPA downloads and renders only a changed part similarly to our SPA proposed in section III. However, a hyperlink click in the PJAX-based SPA always requires that the template be used because the template decides between a partial page update and a full page load, depending on a value of *X-PJAX* (see Fig. 14 and line 5 of Fig. 13(a)). 

The following is a summary of the three applications used in the experiment. 

- *TWA-SW*: an online book publisher. A template and one of the web pages are shown in Fig. 1. Users can write and read reviews on books (see lines 15 and 16 of Fig. 1(a)). In addition, they can obtain information on books (see line 13 of Fig. 1(a)). They can search books by keyword (see lines 5-8 of Fig. 1(a)). The About page (see line 12 of Fig. 1(a)) is provided for introducing the company. The *Initial* page is provided as the first page (main page) of the application which users visit, showing only a template. To reflect the characteristics of real-world web applications from a size perspective, the template of *TWA-SW* includes two images with a total size of 240 KB. 

- *SPA-SW*: a web application into which *TWA-SW* is transformed by applying our approach. 

- *PJAX-SW*: a web application into which *TWA-SW* is transformed by using the PJAX library. When accessing *PJAX-SW* and *SPA-SW*, users usually visit the *Initial* page and then other pages. 

Table II shows the software and hardware environment for the experiment. To compare the performance of the applications, response time is used as a performance index, which is the amount of time from the start of a request from a browser until a response arrives at the browser. For TWAs, onload time [7] is applied, which measures the time from sending an HTTP request until an *onload* event of the window object is triggered by a web browser. The *onload* event is the first event triggered as soon as the entire page is loaded. On the other hand, an SPA does not have the *onload* event except for the first access of the SPA. Thus, the response time of an SPA is defined as the time from sending an AJAX request until the DOM tree of the SPA is updated with a response. 

We need to measure the performance of the applications in a stable state. Therefore, before measuring the performance, all the web pages are visited so that the resources of the pages such as images, JavaScript, and HTML files should be stored in a browser cache, if possible. 

Then, we visit every page and measure the response time and the amount of data transferred in a network. The results (as arithmetic mean) are shown in Fig. 15. Except for the *Initial* page, *SPA-SW* improves the response time of *TWA-SW* by a range of 16% to 96%. *SPA-SW* also improves the response time of *PJAX-SW* by a range of 5% to 91%. The findings are as follows: 
- The *Initial* page: the page shows only the common layout. To revisit the *Initial* page, the refresh button of the browser is used. This is because there is no hyperlink connected to the page in the applications. When refreshing a page in a stable state, static resources such as HTML, images, and JavaScript files are usually already cached in a browser and not downloaded (i.e., HTTP 304 not modified error occurs). However, dynamic resources such as JSPs should be downloaded. Therefore, when accessing the page *Initial, SPA-SW, TWA-SW*, and *PJAX-SW*
download only the response from the template written in JSP. *SPA-SW* and *PJAX-SW* do not improve *TWA-SW* because they process the JavaScript code to enable the AJAX and PJAX, 
respectively. 

- The *About* page: when accessing the page, *SPA-SW*
is much faster. This is because its page-specific part is a static HTML file, so *SPA-SW* uses the file that is cached in a web browser. *TWA-SW* downloads the full page consisting of the common layout and the page-specific part. In the case of *PJAX-SW*, the PJAX request is sent to the template view, because the interaction among web components (see Fig. 

14(b)) is the same as that of *TWA-SW*. The response with only the page-specific part is downloaded. 

- The *Books* page: this page shows information on books in a table layout. The request for obtaining the page is sent to a controller, unlike the two pages previously described. *SPA-SW* and *PJAX-SW* are faster than *TWA-SW* because *TWA-SW* only refreshes a full page. 

- The *WrFmLoad* page: this page loads a form for writing a book review. The request to obtain the page is sent to the template view in *TWA-SW*. When accessing the page, *SPA-SW* is much faster than TWA-SW and *PJAX-SW*. This is because, although a page-specific part of the page is written in JSP, 
unlike in case of the page *About, SPA-SW* bypasses the template view. 

- The *Search* page: this page allows users to search books by keyword. When a user enters a keyword in a text field within a form and submits the form, the GET request is sent to a controller. *PJAX-SW*
refreshes a full page upon form submission, because form submission is not officially supported by the PJAX to our knowledge [16]. Therefore, *SPA-SW* is faster than *TWA-SW* and *PJAX-SW* because *SPA-SW*
only updates a page without refreshing a full page. 

- The *WrFmSbmt* page: this page allows users to write book reviews. When a user enters data in input fields within a form and submits the form, the POST request is sent to a controller. *PJAX-SW* refreshes a full page for reasons mentioned in the previous paragraph. When accessing the page, *SPA-SW* is much faster. 

- The amount of transferred data: when visiting the pages in a stable state, static resources such as HTML, images, and JavaScript files are usually already cached in a browser. However, dynamic resources such as JSPs and Servlets should be downloaded. Therefore, the access by *SPA-SW* to the About page is fastest. 

- The amount of transferred data for the *Initial* page: 
the *Initial* page comprises a template in JSP, images, and JavaScript files. When visiting the page in a stable state, only JSP files are downloaded. 

Therefore, the transferred data of *SPA-SW* and PJAX-SW is larger than that of *TWA-SW* because the template files of *SPA-SW* and *PJAX-SW* are larger. 

URLs in a browser's address bar are often bookmarked and shared. In the second experiment, the performance of the three applications is measured when the applications are first accessed using bookmarked URLs. To that end, the browser cache is cleared before each access to a page. POST requests cannot be correctly bookmarked because none of the form data is shown in a browser's address bar. Thus, the WrFmSbmt page is not included in the second experiment. 

The results are shown in Fig. 16. *SPA-SW* does not improve TWA-SW because *SPA-SW* processes the JavaScript code to enable the AJAX. However, *SPA-SW* performs better that PJAX-SW because *PJAX-SW* needs more time to download 

the PJAX library and to enable the PJAX than *SPA-SW*. It can be seen that our architecture transformation for page refreshes (shown in Fig. 11) does not degrade the performance of *TWA-SW* significantly when compared to the PJAX-based approach. 

![8_image_1.png](8_image_1.png)

10: return; 11: } 
12: %> 

13-29: same as lines 2-18 of Fig. 1(a) **// return a full page like the original TWA 30: <span id="pjax-container">** 
31: <jsp:include page="${param.Body}" /> 
32: </span> 
33-38 30-35: same as lines 20-25 of Fig. 1(a)
(a) Server code 39: <script> 
40: $('a').pjax('#pjax-container'); 
41:</script>
(b) Client code Figure 13. Example of a PJAX-based SPA. TWA of Fig. 1 is transformed 

![8_image_2.png](8_image_2.png)

(a) In the case of using hyperlinks with indirectly referenced templates. 

The TWA architecture of Fig. 4(a) is transformed into this architecture. 

(b) In the case of using hyperlinks with 

directly referenced templates. The TWA 

architecture of Fig. 6(a) is transformed 

into this architecture. 

Figure 14. Transforming architecture for PJAX-based SPA 

TABLE II. EXPERIMENTAL ENVIRONMENT

 Client Web server 

CPU Intel i5-2500 3.3GHz Intel i5-2500 3.3GHz

RAM DDR3 4GB DDR3 4GB

OS Windows 7 32bit Windows 7 32bit

DB Cubrid 2008 R4.1

Web container Tomcat7.0

Web browser Chrome 19.0.1084.56 m

![8_image_3.png](8_image_3.png) 

(a) Response time (ms) (b) Transferred data (KB) 
Figure 15. Performance of SPA-SW, PJAX-SW, and TWA-SW in a stable state 

![8_image_0.png](8_image_0.png) 

(a) Response time (ms) (b) Transferred data (KB) 
Figure 16. Performance of SPA-SW, PJAX-SW, and TWA-SW for the first access to each application 

## Vi. Discussion

In this section, we compare the PJAX-based approach and our approach with respect to functional and nonfunctional quality attributes considered significant in the field of web applications. 

- Efficiency: as described in the previous section, SPA-SW improves *TWA-SW* in a stable state and performs better than or equal to *PJAX-SW* in terms of the response time. When a browser does not support the HTML5 history API, *SPA-SW* also performs better than *PJAX-SW*. This is because users can use *SPA-SW* without refreshing a full page. 

However, *PJAX-SW* is used with a full page refresh. 

- Architectural complexity: *SPA-SW* improves the structure of *TWA-SW* because *SPA-SW* reduces the interaction between web components by bypassing a template. *PJAX-SW* does not change the interaction structure but removes the redundant download of a template via AJAX. In addition, the non-standard HTTP header *X-PJAX* should be used in PJAXbased applications. 

- Automatic transformation: the Eclipse plugin has been developed for reengineering of TWAs in our approach. In our opinion, the PJAX-based reengineering approach can also be automated. 

- Backward/forward navigation: if a browser supports the HTML5 history API, users can go forward and backward through a set of previously visited states within our SPA. On unsupported browsers, while users can use our SPAs without refreshing a full page, such navigation is not possible. In the case of the PJAX-based approach, if a browser does not support the history API, HTTP requests are used so a full page is loaded. Therefore, users can navigate with a back button while refreshing a full page. 

- Bookmarkability: if a browser supports the HTML5 history API, users can bookmark a specific state within our SPA. On unsupported browsers, users can bookmark only the state that was visited first within our SPA. This is because the URL in the browser's address bar does not change. However, when users of supported browsers send a URL to their friend, the friend can view the same state even on unsupported browsers. In the case of the PJAXbased approach, bookmarking is possible independently of the history API support. When accessing to a shared URL, *SPA-SW* performs better than *PJAX-SW* (as shown in Fig. 16). 

- Compatibility: on browsers that do not support the HTML5 history API, *PJAX-SW* fully degrades [16]. 

Therefore, *PJAX-SW* runs while refreshing a full page, similarly to *TWA-SW*. On the unsupported browsers, *SPA-SW* runs without triggering a full page load. However, *SPA-SW* does not provide bookmarking and backward navigation. 

For the HTML history API, Chrome 8+, Safari 5+, 
Firefox 4+, Opera 11.50+, and IPhone 4.2.1+ implement the API [14]. 

## Vii. Related Work

Recently, researchers [11, 18, 19] have proposed web reengineering techniques of transforming legacy MPAs to SPAs. One study [11] proposed a reverse engineering technique that identifies independently updatable user interface elements to obtain an SPA by analyzing MPA web pages. Another study [19] transforms a UI of a legacy MPA 
into a UI of an SPA through incremental refactoring. Another study [18] presented essential RIA (Rich Internet Application) features such as the offline mode and proposed a framework to migrate MPAs to RIAs. Unfortunately, these studies mainly focus on UI redesign without modifying the server code. However, efficient partial page updates require the server code to be analyzed and transformed into a code that sends only the changed data to browsers in response to a request. There have also been several reengineering approaches which modify the server-side of web applications [1, 22, 21]. 

In [1], the authors transform JSP-based web pages that present subsets of a list. These pages include some subsets and hyperlinks to their next or previous pages with other subsets. One example is search result pages of Google. The approach transforms the web pages in two steps using the TXL source transformation language [2]. First, it uses slicing to extract a web service that produces the list data in XML 
format. Second, the list generation code is replaced with AJAX routines which call the service. Thus, the transformed page can contain the next or previous sub-list without downloading the entire page. However, an important problem is that the approach does not consider the transformation of HTML forms. 

A refactoring system FTT [22] was proposed to alleviate problems with traditional HTTP forms. The approach reengineers traditional HTTP forms to AJAX-enabled forms. 

It also considers a form validation problem: the validation is usually invoked upon form submission and the entire page is refreshed. The problem was solved by a validation code generator that enables form validations to be triggered in events such as the *onchange* and *onblur* events other than the onsubmit event. However, that study has some limitations: 
FTT considers only forms, it focuses on JSPs that use the MySQL as a database, and its transformed version is required to use the jQuery library rather than web standards. 

A study [21] also proposed an approach to transform JSP-based applications into AJAX-based applications. The core steps of the transformation process are as follows: first, a template is identified from web pages. An AJAX routine is provided to fill a placeholder in the template by including page-specific data. The next step is to write a controller which forwards a request from an AJAX application to its corresponding JSP, receives a result from the JSP, and then replies to the application with the result. The last step is to remove the template from each JSP file. The hyperlinks and forms in the JSP file are then transformed so that AJAX 
requests can be issued by clicking on them. This transformation process is similar to our research, but its steps are not described in concrete detail. In addition, we fully consider the transformation of traditional forms, unlike the study in [21]. Another limitation is that the transformed application requires the use of the DWR [3] library rather than web standards. 

Our approach differs from the previous work on transformation from legacy MPAs into SPAs. First, we analyze and refactor the server code such that a web server can send only the changed data to a browser, in contrast to client-side analysis approaches in [11, 19, 18]. Second, while other studies [22, 1, 21] also transform the server code as in our approach, they only consider forms or web pages that display a list of data. Thus, the studies are insufficient for application to general TWAs. In contrast, our approach focuses on general Java-based TWAs. Third, our approach complies with web standards, so the transformed SPA 
requires no specific library and plugin. 

## Viii. Conclusion

In template-based web applications, users can easily obtain information through a consistent structure of a template. However, TWAs still have the same interaction problems as traditional web applications, in that each time a user clicks a hyperlink or submits a form, a new page is loaded. 

We proposed a reengineering technique to transform the multi-page structure of a legacy Java-based TWA into a single-page structure with partial page refreshes. This approach refactors hyperlinks and forms in HTML code into elements with AJAX-enabled event handlers to achieve the single-page structure. In addition, JSP/Servlet (server-side) 
and HTML/JavaScript (client-side) code is refactored to send only the data necessary for the partial update. Our experiment shows that our technique improves the response time of TWAs by 16% to 96% in a stable state. 

## Acknowledgment

This research was supported by Basic Science Research Program through the National Research Foundation of Korea 
(NRF) funded by the Ministry of Education, Science and Technology (No. 2012-0008457). This work was supported by the Catholic University of Korea, Research Fund, 2013. 

This research was supported by Basic Science Research Program through the National Research Foundation of Korea 
(NRF) funded by the Ministry of Education, Science and Technology (No. 2011-0013781). 

## References

[1] J. Chu and T. Dean, "Automated Migration of List Based JSP Web Pages to AJAX," Proc. of the 8th IEEE Intl. Working Conf. on Source Code Analysis and Manipulation, 2008. 

[2] J. R. Cordy, T. R. Dean, A. J. Malton, and K. A. Schneider, "Source Transformation in Software Engineering Using the TXL Transformation System," Journal of Information and Software Technology, vol. 44, no. 13, 2002. 

[3] Direct Web Remoting, http://directwebremoting.org. [4] B. G. Estrada, Take Me Back: A Study of the Back Button in the Modern Internet. Ph.D. Dissertation, California Polytechnic State University, 2011. 

[5] J. J. Garrett, "AJAX: A New Approach to Web Applications," 
Adaptive Path, 2005. 

[6] Jericho HTML Parser, http://jericho.htmlparser.net. 

[7] D. Kang, "Web Performance Optimization: Today and Tomorrow," 
Communications of KIISE, vol. 30, no. 5, 2012. 

[8] C. Kim and K. Shim, "TEXT: Automatic Template Extraction from Heterogeneous Web Pages," IEEE Transactions on Knowledge and Data Engineering, vol. 23, no. 4, 2011. 

[9] Y. Kim, JSP & Servlet for Java Programmers. Hanbit Media Press, 2010, Chapter 13. 

[10] R. Kübert, G. Katsaros, and T. Wang, "A RESTful Implementation of the WS-Agreement Specification," Proc. of the 2nd Intl. Workshop on RESTful Design, 2011. 

[11] A. Mesbah and A. Van Deursen, "Migrating Multi-Page Web Applications to Single-Page AJAX Interfaces," Proc. of the 11th European Conf. on Software Maintenance and Reengineering, 2007. 

[12] J. Oh, H. C. Choi, S. H. Lim, and W. H. Ahn, "Reengineering Template-Based Web Applications to Single Page AJAX Applications," KIPS Transactions on Software and Data Engineering, vol. 1, no. 1, 2012. 

[13] T. J. Parr, "Enforcing Strict Model-View Separation in Template Engines," Proc. of WWW 2004, 2004. 

[14] M. Pilgrim, Dive into HTML5. http://diveintohtml5.info/, 2011. 

[15] Y. Ping, K. Kontogiannis, and T. C. Lau, "Transforming Legacy Web Applications to the MVC Architecture," Proc. of 8th Annual Intl. 

Workshop on Software Technology and Engineering Practice, 2003. 

[16] PJAX, https://github.com/defunkt/jquery-pjax. [17] E. Robson, and E. Freeman, Head First HTML with CSS & XHTML. 

O'Reilly Media, 2005. 

[18] R. Rodríguez-Echeverría, J. Conejero, P. Clemente, J. Preciado, and F. Sánchez-Figueroa, "Modernization of Legacy Web Applications into Rich Internet Applications," Proc. of the 11th Intl. Conf. on Current Trends in Web Engineering, 2012. 

[19] G. Rossi, M. Urbieta, J. Ginzburg, D. Distante, and A. Garrido, 
"Refactoring to Rich Internet Applications. A Model-Driven Approach," Proc. of the 8th Intl. Conf. on Web Engineering, 2008. 

[20] G. Seshadri, "Understanding JavaServer Pages Model 2 Architecture," http://www.javaworld.com/javaworld/jw-12-1999/jw12-ssj-jspmvc.html, 1999. 

[21] Q. Wang, Q. Liu, N. Li, and Y. Liu, "An Automatic Approach to Reengineering Common Website with AJAX," Proc. of the 4th Intl. 

Conf. on Next Generation Web Services Practices, 2008. 

[22] M. Ying and M. James, "Refactoring Traditional Forms into AjaxEnabled Forms," Proc. of the 18th Working Conf. on Reverse Engineering, 2011. 