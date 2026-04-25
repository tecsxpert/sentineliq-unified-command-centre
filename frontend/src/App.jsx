import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import LoginPage from './pages/LoginPage'
import ListPage from './pages/ListPage'
import FormPage from './pages/FormPage'
import DashboardPage from './pages/DashboardPage'
import DetailPage from './pages/DetailPage'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={
            <ProtectedRoute><DashboardPage /></ProtectedRoute>
          } />
          <Route path="/records" element={
            <ProtectedRoute><ListPage /></ProtectedRoute>
          } />
          <Route path="/records/:id" element={
            <ProtectedRoute><DetailPage /></ProtectedRoute>
          } />
          <Route path="/create" element={
            <ProtectedRoute><FormPage /></ProtectedRoute>
          } />
          <Route path="/edit/:id" element={
            <ProtectedRoute><FormPage /></ProtectedRoute>
          } />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App