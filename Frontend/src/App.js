import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import About from './pages/About'
import Organizations from './pages/Organizations'
import Courses from './pages/Courses'
import Market from './pages/Market'
import Home from './pages/Home'
import LogIn from './components/Login'
import SignUp from './components/SignUp'
import CoursesHome from './components/CoursesHome'
import AnimalFarming from './components/AnimalFarming'
const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" index element={<Home />} />
        <Route path="/market" element={<Market />} />
        <Route path="/organizations" element={<Organizations />} />
        <Route path="/about" element={<About />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/courseshome" element={<CoursesHome />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/animalfarming" element={<AnimalFarming />} />
        {/* <Route path="*" element={<PageNotFound />} /> */}
      </Routes>
    </BrowserRouter>
  )
}

export default App
