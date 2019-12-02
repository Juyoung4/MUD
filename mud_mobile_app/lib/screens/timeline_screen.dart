import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/models/Conection_error.dart';
import 'package:mud_mobile_app/models/api_models.dart';
import 'package:mud_mobile_app/models/button_models.dart';
import 'package:mud_mobile_app/screens/read_more.dart';
import 'package:mud_mobile_app/services/api_service.dart';
import 'package:mud_mobile_app/services/tts_service.dart';
import 'package:mud_mobile_app/utilities/constants.dart';
import 'dart:async';

class TimelineScreen extends StatefulWidget {
  @override
  _TimelineScreenState createState() => _TimelineScreenState();
}

class _TimelineScreenState extends State<TimelineScreen> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  Future _futureCluster;
  Future _futureArticles;
  bool isSwitched = false;
  List<Clusters> clusters;
  ArticlePagination articlePagination;
  List<AllUserBookmarks> allUserBookmarks = List();
  List<String> bookmarkNewsIds = List();

  getData() async {
    await checkBookmarks();
    return await ApiService.getRecommends();
  }

  getArticles() async {
    await checkBookmarks();
    return await ApiService.getArticles(null);
  }

  void createbookmark(newsId, headline, summary) async {
    bool result = await ApiService.creatBookmark(newsId, headline, summary);
    if (result){
      setState(() {
        bookmarkNewsIds.add(newsId);
      });
      print('Done');
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
  }

  @override
  void initState(){
    super.initState();
    this._futureCluster = getData();
    this._futureArticles = getArticles();
  }

  @override
  Widget build(BuildContext context) {
    final double devHeight = MediaQuery.of(context).size.height;
    final double devWidth = MediaQuery.of(context).size.width;
    final double topPadding = MediaQuery.of(context).padding.top;
    return Scaffold(
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
                            color: Colors.transparent,
                            icon: Icon(Icons.arrow_back_ios, size: 36,),
                            onPressed: (){},
                          ),
                          Text('Today\'s News', style: kTitleStyleMain,),
                          IconButton(
                            color: Colors.white,
                            icon: Icon(Icons.search, size: 36,),
                            onPressed: (){},
                          ),
                        ],
                      ),
                      Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.only(
                            topLeft: Radius.circular(30),
                            topRight: Radius.circular(30),
                          ),
                          color: Colors.white
                        ),
                        padding: EdgeInsets.symmetric(vertical: 10),
                        margin: EdgeInsets.only(top: 10),
                        child: TtsService()
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
            FutureBuilder(
              future: _futureCluster,
              builder: (BuildContext context, AsyncSnapshot snapshot){
                if (snapshot.connectionState == ConnectionState.waiting){
                  return SliverToBoxAdapter(
                    child: Container(
                      height: 200.0,
                      child: CircularProgressIndicator(),
                      alignment: Alignment.center,
                    ),
                  );
                } else if (snapshot.hasError) {
                  return SliverToBoxAdapter(
                    child: Container(
                      child: ErrorDisplay(errorDisplay: 'Opps Somthing is not okay!', error: true,),
                    ),
                  );
                } else if (!snapshot.hasData) {
                  return SliverToBoxAdapter(
                    child: Container(
                      child: ErrorDisplay(errorDisplay: 'You Dont Have Recommends News Yet', error: false,),
                    ),
                  );
                }
                clusters = snapshot.data;
                var childCount = clusters.length;
                return SliverList(
                  delegate: SliverChildBuilderDelegate((BuildContext contex, int index) {
                    return Container(
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
                                clusters[index].clusterHeadline,
                                style: TextStyle(
                                  color: Colors.black,
                                  fontSize: 18.0,
                                  fontWeight: FontWeight.w600,
                                ),
                                overflow: TextOverflow.ellipsis,
                                maxLines: 2,
                              ),
                            ),
                            SizedBox(
                              height: 5.0,
                            ),
                            Container(
                              child: Text(
                                clusters[index].clusterSummary,
                                style: TextStyle(
                                  color: Colors.black87,
                                  fontSize: 16.0,
                                  fontWeight: FontWeight.w400,
                                ),
                                overflow: TextOverflow.ellipsis,
                                maxLines: 3,
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
                            Padding(
                              padding: const EdgeInsets.only(top: 5.0),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceAround,
                                children: <Widget>[
                                  RaisedGradientButton(
                                    child: Row(
                                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                                      children: <Widget>[
                                        Icon(Icons.bookmark, color: Colors.white,),
                                        Text('Bookmark', style: TextStyle(color: Colors.white),)
                                      ],
                                    ),
                                    onPressed: !bookmarkNewsIds.contains(clusters[index].clusterId) ? (){
                                      createbookmark(
                                        clusters[index].clusterId,
                                        clusters[index].clusterHeadline,
                                        clusters[index].clusterSummary,
                                      );
                                    } : (){},
                                    gradient: LinearGradient(
                                      colors: !bookmarkNewsIds.contains(clusters[index].clusterId) ? [
                                        Color(0xFF398AE5),
                                        Color(0xFF73AEF5),
                                      ] : [
                                        Colors.grey,
                                        Colors.grey
                                      ],
                                      begin: Alignment.bottomLeft,
                                      end: Alignment.topRight
                                    ),
                                  ),
                                  RaisedGradientButton(
                                    child: Row(
                                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                                      children: <Widget>[
                                        Icon(Icons.chrome_reader_mode, color: Colors.white,),
                                        Text('Read More', style: TextStyle(color: Colors.white),)
                                      ],
                                    ),
                                    onPressed: (){},
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
                              ),
                            ),
                          ],
                        )
                      ),
                    );
                  },
                  childCount: childCount),
                );
              },
            ),
            FutureBuilder(
              future: _futureArticles,
              builder: (BuildContext context, AsyncSnapshot snapshot){
                if (snapshot.connectionState == ConnectionState.waiting){
                  return SliverToBoxAdapter(
                    child: Container(
                      height: 100.0,
                      child: CircularProgressIndicator(),
                      alignment: Alignment.center,
                    ),
                  );
                } else if (snapshot.hasError || !snapshot.hasData) {
                  return SliverToBoxAdapter(
                    child: Container(
                      child: ErrorDisplay(errorDisplay: 'Opps Somthing is not okay!', error: true,),
                    ),
                  );
                }
                articlePagination = snapshot.data;
                var childCount = articlePagination.results.length;
                return SliverList(
                  delegate: SliverChildBuilderDelegate((BuildContext contex, int index) {
                    return Container(
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
                                articlePagination.results[index].headline == null ? 'Headline' : articlePagination.results[index].headline,
                                style: TextStyle(
                                  color: Colors.black,
                                  fontSize: 18.0,
                                  fontWeight: FontWeight.w600,
                                ),
                                overflow: TextOverflow.ellipsis,
                                maxLines: 2,
                              ),
                            ),
                            SizedBox(
                              height: 5.0,
                            ),
                            Container(
                              child: Text(
                                articlePagination.results[index].summary,
                                style: TextStyle(
                                  color: Colors.black87,
                                  fontSize: 16.0,
                                  fontWeight: FontWeight.w400,
                                ),
                                overflow: TextOverflow.ellipsis,
                                maxLines: 3,
                              ),
                            ),
                            SizedBox(
                              height: 5.0,
                            ),
                            Container(
                                child: Text(
                                  'Publication Date : ' + articlePagination.results[index].pubDate.split("T")[0],
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
                              height: 1,
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.all(Radius.circular(50)),
                                color: Color(0xFF398AE5)
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.only(top: 5.0),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceAround,
                                children: <Widget>[
                                  RaisedGradientButton(
                                    child: Row(
                                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                                      children: <Widget>[
                                        Icon(Icons.bookmark, color: Colors.white,),
                                        Text('Bookmark', style: TextStyle(color: Colors.white),)
                                      ],
                                    ),
                                    onPressed: !bookmarkNewsIds.contains(articlePagination.results[index].newsId) ? (){
                                      createbookmark(
                                        articlePagination.results[index].newsId,
                                        articlePagination.results[index].headline,
                                        articlePagination.results[index].summary,
                                      );
                                    } : (){},
                                    gradient: LinearGradient(
                                      colors: !bookmarkNewsIds.contains(articlePagination.results[index].newsId) ? [
                                        Color(0xFF398AE5),
                                        Color(0xFF73AEF5),
                                      ] : [
                                        Colors.grey,
                                        Colors.grey
                                      ],
                                      begin: Alignment.bottomLeft,
                                      end: Alignment.topRight
                                    ),
                                  ),
                                  RaisedGradientButton(
                                    child: Row(
                                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                                      children: <Widget>[
                                        Icon(Icons.chrome_reader_mode, color: Colors.white,),
                                        Text('Read More', style: TextStyle(color: Colors.white),)
                                      ],
                                    ),
                                    onPressed: (){
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder: (context) => ReadMoreNews(articlePagination.results[index])),
                                      );
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
                              ),
                            ),
                          ],
                        )
                      ),
                    );
                  },
                  childCount: childCount),
                );
              },
            )
          ],
        )
      ),
    );
  }
}