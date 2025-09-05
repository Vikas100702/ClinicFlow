import { useAuth } from '../../contexts/AuthContext'
import './Header.css'

const Header = () => {
  const { user, logout } = useAuth()

  return (
    <header className="header">
      <div className="header-content">
        <h1>ClinicFlow</h1>
        <div className="header-actions">
          <span>Welcome, {user?.full_name}</span>
          <button onClick={logout} className="btn btn-secondary">
            Logout
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header
