import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Suspense } from 'react'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import ErrorBoundary from './components/ErrorBoundary'
import { TableSkeleton, CardGridSkeleton } from './components/Skeleton'
import LoginPage from './pages/LoginPage'
import ListPage from './pages/ListPage'
import FormPage from './pages/FormPage'
import DashboardPage from './pages/DashboardPage'
import DetailPage from './pages/DetailPage'
import AnalyticsPage from './pages/AnalyticsPage'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <ErrorBoundary>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={
              <ProtectedRoute>
                <Suspense fallback={<div style={{padding:'1.5rem'}}><CardGridSkeleton /></div>}>
                  <DashboardPage />
                </Suspense>
              </ProtectedRoute>
            } />
            <Route path="/records" element={
              <ProtectedRoute>
                <Suspense fallback={<div style={{padding:'1.5rem'}}><TableSkeleton /></div>}>
                  <ListPage />
                </Suspense>
              </ProtectedRoute>
            } />
            <Route path="/records/:id" element={
              <ProtectedRoute>
                <Suspense fallback={<div style={{padding:'1.5rem'}}><TableSkeleton /></div>}>
                  <DetailPage />
                </Suspense>
              </ProtectedRoute>
            } />
            <Route path="/create" element={
              <ProtectedRoute>
                <Suspense fallback={<div style={{padding:'1.5rem'}}><TableSkeleton /></div>}>
                  <FormPage />
                </Suspense>
              </ProtectedRoute>
            } />
            <Route path="/edit/:id" element={
              <ProtectedRoute>
                <Suspense fallback={<div style={{padding:'1.5rem'}}><TableSkeleton /></div>}>
                  <FormPage />
                </Suspense>
              </ProtectedRoute>
            } />
            <Route path="/analytics" element={
              <ProtectedRoute>
                <Suspense fallback={<div style={{padding:'1.5rem'}}><CardGridSkeleton /></div>}>
                  <AnalyticsPage />
                </Suspense>
              </ProtectedRoute>
            } />
          </Routes>
        </ErrorBoundary>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App