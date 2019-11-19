import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/screens/category_listview_page.dart';
import 'package:mud_mobile_app/utilities/constants.dart';
import 'package:mud_mobile_app/utilities/fade_in_animation.dart';

class CategoryScreen extends StatefulWidget {
  @override
  _CategoryScreenState createState() => _CategoryScreenState();
}

class _CategoryScreenState extends State<CategoryScreen> {
  @override
  Widget build(BuildContext context) {
    final double devHeight = MediaQuery.of(context).size.height;
    return Scaffold(
      backgroundColor: Colors.white,
      body: AnnotatedRegion<SystemUiOverlayStyle>(
        value: SystemUiOverlayStyle.dark,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Container(
              padding: EdgeInsets.only(bottom: 10.0),
              height: (devHeight / 2) * 0.4,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: <Widget>[
                  Column(
                    mainAxisAlignment: MainAxisAlignment.end,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: <Widget>[
                      Container(
                        child: FadeIn(1.0, Text("News", style: kTopBarTitleStyle)),
                      ),
                      Container(
                        child: FadeIn(1.2, Text("Category", style: kTopBarTitleStyle)),
                      ),
                    ],
                  ),
                  FadeIn(1.4, Container(
                    height: (devHeight / 2) * 0.2,
                    child: Image.asset('assets/images/category.png'),
                    decoration: BoxDecoration(
                      boxShadow: [
                        BoxShadow(
                          color: Colors.greenAccent.withOpacity(0.3),
                          blurRadius: 20.0,
                          spreadRadius: 5.0,
                          offset: Offset(5.0, 5.0)
                        )
                      ]
                    ),
                  ))
                ],
              ),
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
                            color: Colors.greenAccent
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
                            color: Colors.greenAccent
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
                          child: Text("IT", style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),),
                        ),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(30),
                          border: Border.all(
                            width: 3,
                            color: Colors.greenAccent
                          )
                        ),
                      ),
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => CategoryListView("IT_science", "IT")),
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
                          child: Text("World", style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),),
                        ),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(30),
                          border: Border.all(
                            width: 3,
                            color: Colors.greenAccent
                          )
                        ),
                      ),
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => CategoryListView("world", "World")),
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