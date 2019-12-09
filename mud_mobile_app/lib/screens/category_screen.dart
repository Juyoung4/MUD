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

  buildListTile(String name, String title){
    return GestureDetector(
      child: Container(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: <Widget>[
            Row(
              children: <Widget>[
                Icon(Icons.radio_button_checked),
                SizedBox(
                  width: 30.0,
                ),
                Text(title, style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),),
              ],
            ),
            Icon(Icons.arrow_forward_ios),
          ],
        ),
        margin: EdgeInsets.symmetric(horizontal: 20.0, vertical: 10.0),
        padding: EdgeInsets.symmetric(vertical: 10, horizontal: 15.0),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(30),
          border: Border.all(
            width: 3,
            color: Color(0xFF73AEF5)
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black12,
              blurRadius: 6.0,
              offset: Offset(0, 2),
            ),
          ],
        ),
      ),
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => CategoryListView(name, title)),
        );
      },
    );
  }


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
            Expanded(
              child: ListView(
                physics: NeverScrollableScrollPhysics(),
                children: <Widget>[
                  FadeIn(1.0, buildListTile("society", "Society")),
                  FadeIn(1.1, buildListTile("economy", "Economy")),
                  FadeIn(1.2, buildListTile("IT_science", "IT & Science")),
                  FadeIn(1.3, buildListTile("politics", "Politics")),
                ],
              ),
            ),
          ],
        )
      ),
    );
  }
}