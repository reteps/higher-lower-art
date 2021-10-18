import { initializeApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'

const config = {
  apiKey: 'AIzaSyCnMWEQDbAg9jK5LiH37q2JvIegNgqD5GU',
  authDomain: 'higher-lower-art.firebaseapp.com',
  projectId: 'higher-lower-art',
  storageBucket: 'higher-lower-art.appspot.com',
  messagingSenderId: '1031448882593',
  appId: '1:1031448882593:web:84417c93f0364fc4686fe0',
}

const app = initializeApp(config)

const db = getFirestore(app)

export default db
