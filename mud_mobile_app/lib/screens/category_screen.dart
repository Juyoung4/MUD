import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
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
                        child: FadeIn(1.3, Text("Category", style: kTopBarTitleStyle)),
                      ),
                    ],
                  ),
                  FadeIn(1.6, Container(
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
          ],
        )
      ),
    );
  }
}