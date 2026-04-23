import { BrowserRouter, Routes, Route } from 'react-router-dom'
import ListPage from './pages/ListPage'
import FormPage from './pages/FormPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ListPage />} />
        <Route path="/create" element={<FormPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App