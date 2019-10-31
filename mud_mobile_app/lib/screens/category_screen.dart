import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class CategoryScreen extends StatefulWidget {
  @override
  _CategoryScreenState createState() => _CategoryScreenState();
}

class _CategoryScreenState extends State<CategoryScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        primary: true,
        slivers: <Widget>[
          SliverAppBar(
            brightness: Brightness.light,
            expandedHeight: 80.0,
            elevation: 0.0,
            floating: false,
            pinned: true,
            backgroundColor: Color(0xFFFAFAFA),
            flexibleSpace: FlexibleSpaceBar(
              centerTitle: false,
              titlePadding: EdgeInsets.only(left: 16.0, bottom: 8.0),
              title: Text(
                'News By Category',
                style: TextStyle(
                  color: Color(0xFF398AE5),
                  fontFamily: 'OpenSans',
                  fontSize: 30.0,
                  fontWeight: FontWeight.bold,
                  shadows: <Shadow>[
                    Shadow(
                      offset: Offset.zero,
                      blurRadius: 5.0,
                      color: Colors.black45
                    ),
                  ], 
                )
              ),
            ),
          ),
        ],
      ),
    );
  }
}