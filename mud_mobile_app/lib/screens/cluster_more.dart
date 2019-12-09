import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/models/Conection_error.dart';
import 'package:mud_mobile_app/models/api_models.dart';
import 'package:mud_mobile_app/models/button_models.dart';
import 'package:mud_mobile_app/screens/read_more.dart';
import 'package:mud_mobile_app/services/api_service.dart';
import 'package:mud_mobile_app/utilities/constants.dart';

class ClusterMoreNews extends StatefulWidget {
  final Clusters gotCluster;
  ClusterMoreNews(this.gotCluster);
  @override
  _ClusterMoreNewsState createState() => _ClusterMoreNewsState(gotCluster);
}

class _ClusterMoreNewsState extends State<ClusterMoreNews> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  final Clusters cluster;
  _ClusterMoreNewsState(this.cluster);
  Future _futureArticles;
  ArticlePagination articlePagination;

  getArticles() async {
    return await ApiService.getArticlesByClusterId(cluster.clusterId);
  }

  @override
  void initState() {
    super.initState();
    _futureArticles = getArticles();
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
                        padding: EdgeInsets.symmetric(vertical: 20, horizontal: 10),
                        margin: EdgeInsets.only(top: 10),
                        child: cluster.clusterHeadline != null ? Text(
                          cluster.clusterHeadline, 
                          style: TextStyle( 
                            fontSize: 26, 
                            color: Color(0xFF398AE5), 
                            fontWeight: FontWeight.bold,
                          ),
                          overflow: TextOverflow.ellipsis,
                          maxLines: 2,
                        ) : Text('Cluster Headline')
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
                                articlePagination.results[index].headline,
                                style: TextStyle(
                                  color: Colors.black,
                                  fontSize: 26.0,
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
                                mainAxisAlignment: MainAxisAlignment.end,
                                children: <Widget>[
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