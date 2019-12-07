import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/screens/category_listview_page.dart';
import 'package:mud_mobile_app/utilities/constants.dart';
import 'package:mud_mobile_app/utilities/fade_in_animation.dart';
import 'package:mud_mobile_app/utilities/shape_paint.dart';

class CategoryScreen extends StatefulWidget {
  @override
  _CategoryScreenState createState() => _CategoryScreenState();
}

class _CategoryScreenState extends State<CategoryScreen> {
  @override
  Widget build(BuildContext context) {
    final double devHeight = MediaQuery.of(context).size.height;
    final double devWidth = MediaQuery.of(context).size.width;
    return Scaffold(
      backgroundColor: Colors.white,
      body: AnnotatedRegion<SystemUiOverlayStyle>(
        value: SystemUiOverlayStyle.dark,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Stack(
              children: <Widget>[
                CustomPaint(
                  painter: Chevron(),
                  child: Container(
                    height: devHeight * 0.2,
                    width: devWidth,
                    child: Padding(
                      padding: EdgeInsets.symmetric(horizontal: 20),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: <Widget>[
                          IconButton(
                            color: Colors.transparent,
                            icon: Icon(Icons.arrow_back_ios, size: 36,),
                            onPressed: (){},
                          ),
                          Text('News Category', style: kTitleStyleMain,),
                          IconButton(
                            color: Colors.white,
                            icon: Icon(Icons.search, size: 36,),
                            onPressed: (){},
                          ),
                        ],
                      ),
                    )
                  ),
                )
              ],
            ),
            SizedBox(
              height: 20,
            ),
            Expanded(
              child: FadeIn(1.9, GridView.count(
                padding: EdgeInsets.all(20.0),
                crossAxisSpacing: 8.0,
                mainAxisSpacing: 8.0,
                crossAxisCount: 2,
                children: <Widget>[
                  Card(
                    elevation: 4.0,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30)
                    ),
                    child: GestureDetector(
                      child: Container(
                        height: double.infinity,
                        child: Center(
                          child: Text("Society", style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),),
                        ),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(30),
                          border: Border.all(
                            width: 3,
                            color: Color(0xFF73AEF5)
                          )
                        ),
                      ),
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => CategoryListView("society", "Society")),
                        );
                      },
                    ),
                  ),
                  Card(
                    elevation: 4.0,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30)
                    ),
                    child: GestureDetector(
                      child: Container(
                        height: double.infinity,
                        child: Center(
                          child: Text("Economy", style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),),
                        ),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(30),
                          border: Border.all(
                            width: 3,
                            color: Color(0xFF73AEF5)
                          )
                        ),
                      ),
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => CategoryListView("economy", "Economy")),
                        );
                      },
                    ),
                  ),
                  Card(
                    elevation: 4.0,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30)
                    ),
                    child: GestureDetector(
                      child: Container(
                        height: double.infinity,
                        child: Center(
                          child: Text("IT & Science", style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),),
                        ),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(30),
                          border: Border.all(
                            width: 3,
                            color: Color(0xFF73AEF5)
                          )
                        ),
                      ),
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => CategoryListView("IT_science", "IT & Science")),
                        );
                      },
                    ),
                  ),
                  Card(
                    elevation: 4.0,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30)
                    ),
                    child: GestureDetector(
                      child: Container(
                        height: double.infinity,
                        child: Center(
                          child: Text("Politics", style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),),
                        ),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(30),
                          border: Border.all(
                            width: 3,
                            color: Color(0xFF73AEF5)
                          )
                        ),
                      ),
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => CategoryListView("politics", "Politics")),
                        );
                      },
                    ),
                  ),
                ],
              )),
            )
          ],
        )
      ),
    );
  }
}