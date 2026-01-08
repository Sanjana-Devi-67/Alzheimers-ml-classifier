// import { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { useAuth } from '../context/AuthContext';
// import axios from 'axios';
// import toast from 'react-hot-toast';
// import {
//   Avatar, Button, TextField, Link, Grid, Box, Typography, Paper,
// } from '@mui/material';
// import LockOutlinedIcon from '@mui/icons-material/LockOutlined';

// const Login = () => {
//   const navigate = useNavigate();
//   const { login } = useAuth();
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');

//   const handleSubmit = async (event) => {
//     event.preventDefault();
//     const loadingToast = toast.loading('Signing in...');

//     const formData = new URLSearchParams();
//     formData.append('username', email); 
//     formData.append('password', password);

//     try {
//       const response = await axios.post('http://localhost:8000/api/users/login', formData, {
//         headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
//       });
      
//       const { access_token } = response.data;
//       login(access_token); // Pass the token to the context
      
//       toast.success('Signed in successfully!', { id: loadingToast });
//       navigate('/');
//     } catch (error) {
//       const errorMessage = error.response?.data?.detail || 'Login failed. Please check your credentials.';
//       toast.error(errorMessage, { id: loadingToast });
//       console.error('Login error:', error);
//     }
//   };

//   return (
//     <Paper elevation={6} sx={{ p: 4, borderRadius: 2 }}>
//       <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
//         <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}><LockOutlinedIcon /></Avatar>
//         <Typography component="h1" variant="h5">Sign in</Typography>
//         <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
//           <TextField margin="normal" required fullWidth label="Email Address" autoComplete="email" autoFocus value={email} onChange={(e) => setEmail(e.target.value)} />
//           <TextField margin="normal" required fullWidth name="password" label="Password" type="password" autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} />
//           <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>Sign In</Button>
//           <Grid container>
//             <Grid>
//               <Link href="/signup" variant="body2">{"Don't have an account? Sign Up"}</Link>
//             </Grid>
//           </Grid>
//         </Box>
//       </Box>
//     </Paper>
//   );
// };

// export default Login;
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import toast from 'react-hot-toast';
import {
  Avatar, Button, TextField, Link, Grid, Box, Typography, Paper,
} from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const loadingToast = toast.loading('Signing in...');

    const formData = new URLSearchParams();
    formData.append('username', email); 
    formData.append('password', password);

    try {
      const response = await axios.post('http://localhost:8000/api/users/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      
      const { access_token } = response.data;
      login(access_token);

      toast.success('Signed in successfully!', { id: loadingToast });
      navigate('/');
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Login failed. Please check your credentials.';
      toast.error(errorMessage, { id: loadingToast });
      console.error('Login error:', error);
    }
  };

  return (
    <Paper elevation={6} sx={{ p: 4, borderRadius: 2 }}>
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}><LockOutlinedIcon /></Avatar>
        <Typography component="h1" variant="h5">Sign in</Typography>
        <Box
          component="form"
          onSubmit={handleSubmit}
          noValidate
          autoComplete="off"    // Disable form autocomplete
          sx={{ mt: 1 }}
        >
          <TextField
            margin="normal"
            required
            fullWidth
            label="Email Address"
            autoComplete="new-email"    // Prevent autofill
            name="new-email"            // Change field name so browser does not detect it
            autoFocus
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            label="Password"
            type="password"
            autoComplete="new-password" // Prevent autofill
            name="new-password"         // Change field name to avoid autofill
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
            Sign In
          </Button>
          <Grid container>
            <Grid>
              <Link href="/signup" variant="body2">
                {"Don't have an account? Sign Up"}
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Paper>
  );
};

export default Login;
