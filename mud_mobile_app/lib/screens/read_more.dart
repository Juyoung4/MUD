import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:mud_mobile_app/models/api_models.dart';
import 'package:mud_mobile_app/models/button_models.dart';
import 'package:mud_mobile_app/services/api_service.dart';
import 'package:mud_mobile_app/utilities/constants.dart';
import 'package:url_launcher/url_launcher.dart';

class ReadMoreNews extends StatefulWidget {
  final Results gotNews;
  ReadMoreNews(this.gotNews);
  @override
  _ReadMoreNewsState createState() => _ReadMoreNewsState(gotNews);
}

class _ReadMoreNewsState extends State<ReadMoreNews> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  final Results news;
  _ReadMoreNewsState(this.news);
  List<UserRating> userRating = List();
  double _rating = 0.0;
  bool didRate = false;
  bool didUpdate = false;
  bool didBookmarked = false;
  String ratingId;
  List<AllUserBookmarks> allUserBookmarks = List();
  List<String> bookmarkNewsIds = List();
  Future<void> _launched;

  Future getUserRating() async {
    userRating = await ApiService.getUserRating();
    if (userRating != null){
      for (var i = 0; i < userRating.length; i++){
        if (userRating[i].newsSummary == news.newsId){
          setState(() {
            _rating = userRating[i].score.toDouble();
            didRate = true;
            ratingId = userRating[i].ratingId;
          });
        }
      }
    }
  }

  void createRating() async {
    bool result = await ApiService.creatRating(_rating.toString(), news.newsId);
    print(result.toString());
    return;
  }

  void updateRating() async {
    bool result = await ApiService.updateRating(_rating.toString(), news.newsId, ratingId);
    print(result.toString());
    return;
  }

  Future<bool> _onWillPop() async {
    if (didUpdate && didRate) {
      updateRating();
    } else if (didUpdate && !didRate) {
      createRating();
    }
    return true;
  }

  void createbookmark(newsId, headline, summary) async {
    bool result = await ApiService.creatBookmark(newsId, headline, summary);
    if (result){
      checkBookmarks();
      _scaffoldKey.currentState.showSnackBar(
      SnackBar(
        content: Row(
          children: <Widget>[
            Icon(Icons.save_alt),
            SizedBox(width: 5,),
            Text('Saved'),
          ],
        ),
        duration: Duration(seconds: 2),
      ));
    } else {
      print('Not Done');
      _scaffoldKey.currentState.showSnackBar(
      SnackBar(
        content: Row(
          children: <Widget>[
            Icon(Icons.error),
            SizedBox(width: 5,),
            Text('Opps Not saved'),
          ],
        ),
        duration: Duration(seconds: 2),
      ));
    }
  }

  Future checkBookmarks() async {
    allUserBookmarks = await ApiService.getBookmarksByUser();
    if (allUserBookmarks?.isNotEmpty ?? false){
      for (var i = 0; i < allUserBookmarks.length; i++){
        bookmarkNewsIds.add(allUserBookmarks[i].newsId);
      }
    }
    if (bookmarkNewsIds.contains(news.newsId)){
      setState(() {
        didBookmarked = true;
      });
    } else {
      setState(() {
        didBookmarked = false;
      });
    }
  }

  Future<void> _launchInWebViewWithJavaScript(String url) async {
    if (await canLaunch(url)) {
      await launch(
        url,
        forceSafariVC: true,
        forceWebView: true,
        enableJavaScript: true,
      );
    } else {
      throw 'Could not launch $url';
    }
  }

  Widget _launchStatus(BuildContext context, AsyncSnapshot<void> snapshot) {
    if (snapshot.hasError) {
      return Text('Error: ${snapshot.error}');
    } else {
      return const Text('');
    }
  }

  @override
  void initState() {
    super.initState();
    getUserRating();
    checkBookmarks();
  }

  @override
  Widget build(BuildContext context) {
    final double devHeight = MediaQuery.of(context).size.height;
    final double devWidth = MediaQuery.of(context).size.width;
    final double topPadding = MediaQuery.of(context).padding.top;
    return WillPopScope(
      onWillPop: _onWillPop,
      child: Scaffold(
        key: _scaffoldKey,
        backgroundColor: Colors.white,
        body: AnnotatedRegion<SystemUiOverlayStyle>(
          value: SystemUiOverlayStyle.dark,
          child: CustomScrollView(
            slivers: <Widget>[
              SliverAppBar(
                backgroundColor: Colors.transparent,
                pinned: false,
                expandedHeight: devHeight * 0.2 + topPadding,
                brightness: Brightness.light,
                automaticallyImplyLeading: false,
                flexibleSpace: FlexibleSpaceBar(
                  collapseMode: CollapseMode.parallax,
                  background: Container(
                    height: devHeight * 0.2,
                    width: devWidth,
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: <Widget>[
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          mainAxisAlignment: MainAxisAlignment.spaceAround,
                          children: <Widget>[
                            IconButton(
                              color: Colors.white,
                              icon: Icon(Icons.arrow_back_ios, size: 36,),
                              onPressed: (){
                                if (didUpdate && didRate) {
                                  updateRating();
                                } else if (didUpdate && !didRate) {
                                  createRating();
                                }
                                Navigator.pop(context);
                              },
                            ),
                            Text('NewSum', style: kTitleStyleMain,),
                            IconButton(
                              color: Colors.transparent,
                              icon: Icon(Icons.search, size: 36,),
                              onPressed: (){},
                            ),
                          ],
                        ),
                        Container(
                          width: devWidth,
                          alignment: Alignment.center,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.only(
                              topLeft: Radius.circular(30),
                              topRight: Radius.circular(30),
                            ),
                            color: Colors.white
                          ),
                          padding: EdgeInsets.symmetric(vertical: 10),
                          margin: EdgeInsets.only(top: 10),
                          child: Text('Read More', style: TextStyle(fontFamily: 'Pacifico', fontSize: 36, color: Color(0xFF398AE5), fontWeight: FontWeight.bold,))
                        )
                      ],
                    ),
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                        colors: [Color(0xFF398AE5), Color(0xFF73AEF5)],
                        tileMode: TileMode.clamp,
                      )
                    ),
                  ),
                ),
              ),
              SliverToBoxAdapter(
                child: Container(
                  child: Container(
                    margin: EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
                    padding: EdgeInsets.symmetric(horizontal: 8.0, vertical: 8.0),
                    decoration: BoxDecoration(
                      border: Border.all(
                        width: 1.0,
                        color: Color(0xFF398AE5),
                      ),
                      borderRadius: BorderRadius.all(Radius.circular(5.0))
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: <Widget>[
                        Container(
                          child: Text(
                            news.headline ?? 'Not Found',
                            style: TextStyle(
                              color: Colors.black,
                              fontSize: 28.0,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                        SizedBox(
                          height: 5.0,
                        ),
                        Container(
                          height: 1,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.all(Radius.circular(50)),
                            color: Color(0xFF398AE5)
                          ),
                        ),
                        SizedBox(
                          height: 5.0,
                        ),
                        Container(
                          child: Text(
                            news.summary ?? 'Not Found',
                            style: TextStyle(
                              color: Colors.black87,
                              fontSize: 22.0,
                              fontWeight: FontWeight.w400,
                            ),
                          ),
                        ),
                        SizedBox(
                          height: 5.0,
                        ),
                        Container(
                          height: 1,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.all(Radius.circular(50)),
                            color: Color(0xFF398AE5)
                          ),
                        ),
                        SizedBox(
                          height: 5.0,
                        ),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: <Widget>[
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: <Widget>[
                                Container(
                                  child: Text(
                                    'Category : ' + news.category.toUpperCase() ?? 'Not Found',
                                    style: TextStyle(
                                      color: Colors.black54,
                                      fontSize: 14.0,
                                      fontWeight: FontWeight.w400,
                                    ),
                                  ),
                                ),
                                SizedBox(
                                  height: 5.0,
                                ),
                                Container(
                                  child: Text(
                                    'Publication Date : ' + news.pubDate.split("T")[0] ?? 'Not Found',
                                    style: TextStyle(
                                      color: Colors.black54,
                                      fontSize: 14.0,
                                      fontWeight: FontWeight.w400,
                                    ),
                                  ),
                                ),
                                SizedBox(
                                  height: 5.0,
                                ),
                                Container(
                                  child: Text(
                                    'Summarized Data : ' + news.sumDate.split("T")[0] ?? 'Not Found',
                                    style: TextStyle(
                                      color: Colors.black54,
                                      fontSize: 14.0,
                                      fontWeight: FontWeight.w400,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            RaisedGradientButton(
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceAround,
                                children: <Widget>[
                                  Icon(Icons.bookmark, color: Colors.white,),
                                  Text('Bookmark', style: TextStyle(color: Colors.white),)
                                ],
                              ),
                              onPressed: !didBookmarked ? (){
                                createbookmark(
                                  news.newsId,
                                  news.headline,
                                  news.summary,
                                );
                              } : (){},
                              gradient: LinearGradient(
                                colors: didBookmarked ? [
                                  Colors.grey,
                                  Colors.grey,
                                ] : [
                                  Color(0xFF398AE5),
                                  Color(0xFF73AEF5),
                                ],
                                begin: Alignment.bottomLeft,
                                end: Alignment.topRight
                              ),
                            ),
                          ],
                        ),
                        SizedBox(
                          height: 5.0,
                        ),
                        Container(
                          height: 1,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.all(Radius.circular(50)),
                            color: Color(0xFF398AE5)
                          ),
                        ),
                        Padding(
                          padding: const EdgeInsets.only(top: 5.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: <Widget>[
                              Container(
                                alignment: Alignment.center,
                                child: RatingBar(
                                  initialRating: _rating,
                                  itemCount: 5,
                                  itemBuilder: (context, index){
                                    switch (index) {
                                      case 0:
                                        return Icon(
                                            Icons.sentiment_very_dissatisfied,
                                            color: Colors.red,
                                        );
                                      case 1:
                                        return Icon(
                                            Icons.sentiment_dissatisfied,
                                            color: Colors.redAccent,
                                        );
                                      case 2:
                                        return Icon(
                                            Icons.sentiment_neutral,
                                            color: Colors.amber,
                                        );
                                      case 3:
                                        return Icon(
                                            Icons.sentiment_satisfied,
                                            color: Colors.lightGreen,
                                        );
                                      case 4:
                                        return Icon(
                                          Icons.sentiment_very_satisfied,
                                          color: Colors.green,
                                        );
                                      default:
                                        return Icon(
                                          Icons.sentiment_very_satisfied,
                                          color: Colors.green,
                                        );
                                    }
                                  },
                                  onRatingUpdate: (rating) {
                                    setState(() {
                                      _rating = rating;
                                      didUpdate = true;
                                    });
                                  },
                                )
                              ),
                              RaisedGradientButton(
                                width: 150,
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                                  children: <Widget>[
                                    Icon(Icons.chrome_reader_mode, color: Colors.white,),
                                    Text('Read Article', style: TextStyle(color: Colors.white),)
                                  ],
                                ),
                                onPressed: (){
                                  setState(() {
                                    _launched = _launchInWebViewWithJavaScript(news.url);
                                  });
                                },
                                gradient: LinearGradient(
                                  colors: [
                                    Color(0xFF398AE5),
                                    Color(0xFF73AEF5),
                                  ],
                                  begin: Alignment.bottomLeft,
                                  end: Alignment.topRight
                                ),
                              ),
                            ],
                          )
                        ),
                        Container(
                          padding: EdgeInsets.symmetric(vertical: 5.0),
                          alignment: Alignment.center,
                          child: FutureBuilder<void>(
                            future: _launched,
                            builder: _launchStatus,
                          ),
                        ),
                      ],
                    )
                  ),
                ),
              )
            ],
          )
        ),
      ),
    );
  }
}