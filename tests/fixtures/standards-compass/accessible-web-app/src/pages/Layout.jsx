export default function Layout({ children, title }) {
  return (
    <div lang="en">
      <a className="skip-link" href="#main">
        Skip to main content
      </a>
      <header>
        <nav aria-label="Primary">
          <ul>
            <li><a href="/appointments">Appointments</a></li>
            <li><a href="/records">Records</a></li>
            <li><a href="/account">Account</a></li>
          </ul>
        </nav>
      </header>
      <main id="main">
        <h1>{title}</h1>
        {children}
      </main>
      <footer>
        <p>Need help? Call the clinic on 0800 000 0000.</p>
      </footer>
    </div>
  )
}
