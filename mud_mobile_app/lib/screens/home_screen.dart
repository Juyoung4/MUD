import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/screens/category_screen.dart';
import 'package:mud_mobile_app/screens/profile_screen.dart';
import 'package:mud_mobile_app/screens/timeline_screen.dart';
import 'package:mud_mobile_app/services/auth_service.dart';
import 'package:mud_mobile_app/utilities/constants.dart';

class HomeScreen extends StatefulWidget {
  static final id = "home_screen";
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {

  int _currentTab = 0;
  PageController _pageController;

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: AnnotatedRegion<SystemUiOverlayStyle>(
        value: SystemUiOverlayStyle.dark,
        child: PageView(
          controller: _pageController,
          children: <Widget>[
            TimelineScreen(),
            CategoryScreen(),
            ProfileScreen(),
          ],
          onPageChanged: (int index) {
            setState(() {
              _currentTab = index;
            });
          },
        ),
      ),
      bottomNavigationBar: CupertinoTabBar(
        currentIndex: _currentTab,
        onTap: (int index) {
          setState(() {
            _currentTab = index;
          });
          _pageController.animateToPage(index, duration: Duration(milliseconds: 200), curve: Curves.easeIn);
        },
        activeColor: Color(0xFF398AE5),
        items: [
          BottomNavigationBarItem(
            icon: Icon(
              Icons.home,
              size: 32.0,
            )
          ),
          BottomNavigationBarItem(
            icon: Icon(
              Icons.menu,
              size: 32.0,
            )
          ),
          BottomNavigationBarItem(
            icon: Icon(
              Icons.person,
              size: 32.0,
            )
          ),
        ],
      )
    );
  }
}