import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';

final myHintTextStyle = TextStyle(
  color: Colors.white54,
  fontFamily: 'OpenSans',
);

final bacgroundColors = [
  Color(0xFF73AEF5),
  Color(0xFF61A4F1),
  Color(0xFF478DE0),
  Color(0xFF398AE5),
];

final myLabelStyle = TextStyle(
  color: Colors.white,
  fontWeight: FontWeight.bold,
  fontFamily: 'OpenSans',
);

final myTitleStyle = TextStyle(
  color: Colors.white,
  fontWeight: FontWeight.bold,
  fontFamily: 'Pacifico',
  fontSize: 46,
  shadows: <Shadow>[
    Shadow(
      offset: Offset.zero,
      blurRadius: 5.0,
      color: Color(0xFF398AE5)
    ),
  ], 
);

final myTextStyle = TextStyle(
  color: Colors.white,
  fontFamily: 'OpenSans',
  fontSize: 20.0,
  fontWeight: FontWeight.bold,
);

final myProfileTextStyle = TextStyle(
  color: Colors.black45,
  fontFamily: 'OpenSans',
  fontSize: 20.0,
  letterSpacing: 1.5,
  fontWeight: FontWeight.bold,
);

final myTextStyleDark = TextStyle(
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
);

final myBoxDecorationStyle = BoxDecoration(
  color: Color(0xFF6CA8F1),
  borderRadius: BorderRadius.circular(10.0),
  boxShadow: [
    BoxShadow(
      color: Colors.black12,
      blurRadius: 6.0,
      offset: Offset(0, 2),
    ),
  ],
);

final _firestore = Firestore.instance;

final usersRef = _firestore.collection('users');