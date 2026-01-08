// import { useState, useEffect, useRef } from 'react';
// import { useParams } from 'react-router-dom';
// import { Box, Typography, Paper, Grid, List, ListItem, ListItemText, Divider, CircularProgress, Button } from '@mui/material';
// import { Doughnut } from 'react-chartjs-2';
// import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
// import toast from 'react-hot-toast';
// import apiClient from '../api/axiosConfig';
// import PredictionModel from '../components/PredictionModel';
// import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
// import DownloadIcon from '@mui/icons-material/Download';
// import jsPDF from 'jspdf';
// import html2canvas from 'html2canvas';

// ChartJS.register(ArcElement, Tooltip, Legend);

// const PatientDetails = () => {
//   const { id } = useParams();
//   const [patient, setPatient] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [isModalOpen, setIsModalOpen] = useState(false);
//   const reportRef = useRef();

//   const fetchPatientDetails = async () => {
//     setLoading(true);
//     try {
//       const response = await apiClient.get(`/patients/${id}`);
//       setPatient(response.data);
//     } catch (error) {
//       toast.error('Failed to fetch patient details.');
//       setPatient(null);
//     } finally {
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     fetchPatientDetails();
//   }, [id]);
  
//   const handleDownloadReport = () => {
//     if (!reportRef.current) { return toast.error("Report content not available."); }
//     const input = reportRef.current;
//     html2canvas(input, { scale: 2 })
//       .then((canvas) => {
//         const imgData = canvas.toDataURL('image/png');
//         const pdf = new jsPDF('p', 'mm', 'a4');
//         const pdfWidth = pdf.internal.pageSize.getWidth();
//         const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
//         pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
//         pdf.save(`patient-report-${patient.name.replace(/\s/g, '_')}-${id}.pdf`);
//         toast.success('Report Downloaded!');
//       });
//   };

//   if (loading) { return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>; }
  
//   // This is the line with the corrected syntax
//   if (!patient) { return <Typography variant="h5" align="center" sx={{ mt: 4 }}>Patient not found or failed to load.</Typography>; }

//   const latestPrediction = patient.predictions.length > 0 ? patient.predictions[patient.predictions.length - 1] : null;
//   const gaugeChartData = {
//     labels: ['Confidence', ''],
//     datasets: [{
//       data: latestPrediction ? [latestPrediction.confidence_score * 100, 100 - (latestPrediction.confidence_score * 100)] : [0, 100],
//       backgroundColor: [ latestPrediction?.prediction_result === "You have Alzheimer's Disease(AD)" ? 'rgba(255, 99, 132, 0.8)' : 'rgba(75, 192, 192, 0.8)', 'rgba(230, 230, 230, 0.8)'],
//       borderColor: ['rgba(255, 255, 255, 0)'],
//       borderWidth: 1, circumference: 180, rotation: -90,
//     }]
//   };
//   const gaugeChartOptions = {
//     responsive: true, maintainAspectRatio: true, cutout: '75%',
//     plugins: { legend: { display: false }, tooltip: { enabled: false } }
//   };

//   return (
//     <Box>
//        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
//         <Typography variant="h4" gutterBottom>Patient Details for {patient.name}</Typography>
//         <Box>
//             <Button variant="outlined" startIcon={<DownloadIcon />} onClick={handleDownloadReport} sx={{ mr: 2 }}>Download Report</Button>
//             <Button variant="contained" startIcon={<AddCircleOutlineIcon />} onClick={() => setIsModalOpen(true)}>Start New Analysis</Button>
//         </Box>
//       </Box>
//       <Box ref={reportRef} sx={{ p: 2, backgroundColor: 'white' }}>
//         <Grid container spacing={3}>
//             <Grid item xs={12} md={4}>
//               <Paper sx={{ p: 2, height: '100%' }}>
//                 <Typography variant="h6" gutterBottom>Information</Typography>
//                 <List>
//                   <ListItem><ListItemText primary="Name" secondary={patient.name} /></ListItem><Divider />
//                   <ListItem><ListItemText primary="Age" secondary={patient.age} /></ListItem><Divider />
//                   <ListItem><ListItemText primary="Gender" secondary={patient.gender} /></ListItem>
//                 </List>
//               </Paper>
//             </Grid>
//             <Grid item xs={12} md={8}>
//                 <Paper sx={{ p: 2, mb: 3, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
//                     <Typography variant="h6" gutterBottom>Most Recent Analysis</Typography>
//                     {latestPrediction ? ( <Box sx={{ position: 'relative', width: '250px', height: '125px' }}>
//                        {/* <Doughnut data={gaugeChartData} options={gaugeChartOptions} /> */}
//                         <Box sx={{ position: 'absolute', top: '65%', left: '50%', transform: 'translate(-50%, -50%)', textAlign: 'center', width: '100%' }}> <Typography variant="h4" component="div">{(latestPrediction.confidence_score * 100).toFixed(1)}%</Typography> <Typography variant="body1" component="div" sx={{ color: latestPrediction.prediction_result === "You have Alzheimer's Disease(AD)" ? 'error.main' : 'primary.main', fontWeight: 'bold', fontSize: '0.9rem', lineHeight: 1.2 }}>{latestPrediction.prediction_result}</Typography> </Box> </Box> ) : ( <Typography sx={{ mt: 4, mb: 4}}>No prediction data available.</Typography> )}
//                 </Paper>
//                 <Paper sx={{ p: 2 }}>
//                     <Typography variant="h6" gutterBottom>Prediction History</Typography>
//                     <List>
//                         {patient.predictions.length > 0 ? patient.predictions.map((p) => (
//                             <ListItem key={p._id}>
//                                 <ListItemText primary={`${new Date(p.created_at).toLocaleString()}: ${p.prediction_result}`} secondary={`Confidence: ${(p.confidence_score * 100).toFixed(1)}%`} />
//                             </ListItem>
//                         )) : ( <ListItem><ListItemText primary="No prediction history found." /></ListItem> )}
//                     </List>
//                 </Paper>
//             </Grid>
//         </Grid>
//       </Box>
//       <PredictionModel open={isModalOpen} handleClose={() => setIsModalOpen(false)} patientId={id} onPredictionSaved={fetchPatientDetails}/>
//     </Box>
//   );
// };

// export default PatientDetails;
import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Typography, Paper, Grid, List, ListItem, ListItemText, Divider, CircularProgress, Button } from '@mui/material';
import { Doughnut, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import toast from 'react-hot-toast';
import apiClient from '../api/axiosConfig';
import PredictionModal from '../components/PredictionModel';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import DownloadIcon from '@mui/icons-material/Download';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

const PatientDetails = () => {
  const { id } = useParams();
  const [patient, setPatient] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const reportRef = useRef();

  const fetchPatientDetails = async () => {
    setLoading(true);
    try {
      const response = await apiClient.get(`/patients/${id}`);
      setPatient(response.data);
    } catch (error) {
      toast.error('Failed to fetch patient details.');
      setPatient(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchPatientDetails(); }, [id]);
  
  const handleDownloadReport = () => {
    if (!reportRef.current) { return toast.error("Report content not available."); }
    const input = reportRef.current;
    html2canvas(input, { scale: 2 }).then((canvas) => {
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('p', 'mm', 'a4');
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
        pdf.save(`patient-report-${patient.name.replace(/\s/g, '_')}-${id}.pdf`);
        toast.success('Report Downloaded!');
      });
  };

  if (loading) { return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>; }
  if (!patient) { return <Typography variant="h5" align="center" sx={{ mt: 4 }}>Patient not found or failed to load.</Typography>; }

  const latestPrediction = patient.predictions.length > 0 ? patient.predictions[patient.predictions.length - 1] : null;
  
  // Feature Importance Chart Data (Horizontal Bar)
  const featureChartData = {
      labels: latestPrediction?.top_features ? latestPrediction.top_features.map(f => f.feature).reverse() : [],
      datasets: [{
          label: 'Impact',
          data: latestPrediction?.top_features ? latestPrediction.top_features.map(f => f.importance).reverse() : [],
          backgroundColor: 'rgba(0, 121, 107, 0.6)',
          borderColor: 'rgba(0, 121, 107, 1)',
          borderWidth: 1,
      }]
  };
  const featureChartOptions = { indexAxis: 'y', responsive: true, plugins: { legend: { display: false } } };

  return (
    <Box>
       <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: { xs: 'flex-start', sm: 'center' }, flexDirection: { xs: 'column', sm: 'row' }, mb: 2 }}>
        <Typography variant="h4" gutterBottom sx={{ mb: { xs: 2, sm: 0 } }}>Patient Details for {patient.name}</Typography>
        <Box sx={{ display: 'flex' }}>
            <Button variant="outlined" startIcon={<DownloadIcon />} onClick={handleDownloadReport} sx={{ mr: 2 }}>Download Report</Button>
            <Button variant="contained" startIcon={<AddCircleOutlineIcon />} onClick={() => setIsModalOpen(true)}>Start New Analysis</Button>
        </Box>
      </Box>
      <Box ref={reportRef} sx={{ p: 2, backgroundColor: 'white' }}>
        <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 2, height: '100%' }}>
                <Typography variant="h6" gutterBottom>Information</Typography>
                <List>
                  <ListItem><ListItemText primary="Name" secondary={patient.name} /></ListItem><Divider />
                  <ListItem><ListItemText primary="Age" secondary={patient.age} /></ListItem><Divider />
                  <ListItem><ListItemText primary="Gender" secondary={patient.gender} /></ListItem>
                </List>
              </Paper>
            </Grid>
            <Grid item xs={12} md={8}>
                <Box>
                    <Paper sx={{ p: 2, mb: 3 }}>
                        <Typography variant="h6" gutterBottom align="center">Most Recent Analysis</Typography>
                        {latestPrediction ? (
                            <Box sx={{ textAlign: 'center' }}>
                                <Typography variant="h4" color={latestPrediction.prediction_result === "Alzheimer's Disease (AD)" ? 'error' : 'primary'} fontWeight="bold">
                                    {latestPrediction.prediction_result}
                                </Typography>
                                
                                {/* SHOW STAGE HERE */}
                                {latestPrediction.stage && latestPrediction.stage !== "N/A" && (
                                    <Typography variant="h6" color="secondary" sx={{ mt: 1 }}>
                                        Stage: {latestPrediction.stage}
                                    </Typography>
                                )}

                                {/* <Typography variant="body1" color="textSecondary" sx={{ mb: 2 }}>
                                    Confidence: {(latestPrediction.confidence_score * 100).toFixed(1)}%
                                </Typography> */}
                                
                            </Box>
                        ) : ( <Typography align="center" sx={{ mt: 4, mb: 4}}>No prediction data available.</Typography> )}
                    </Paper>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6" gutterBottom>Prediction History</Typography>
                        <List>
                            {patient.predictions.length > 0 ? patient.predictions.map((p) => (
                                <ListItem key={p._id}>
                                    <ListItemText 
                                        primary={`${new Date(p.created_at).toLocaleString()}: ${p.prediction_result}`} 
                                        secondary={
                                            <>
                                                {/* <Typography component="span" variant="body2">Confidence: {(p.confidence_score * 100).toFixed(1)}%</Typography> */}
                                                {p.stage && p.stage !== "N/A" && (
                                                    <Typography component="span" variant="body2" color="secondary" sx={{ ml: 2 }}>Stage: {p.stage}</Typography>
                                                )}
                                            </>
                                        }
                                    />
                                </ListItem>
                            )) : ( <ListItem><ListItemText primary="No prediction history found." /></ListItem> )}
                        </List>
                    </Paper>
                </Box>
            </Grid>
        </Grid>
      </Box>
      <PredictionModal open={isModalOpen} handleClose={() => setIsModalOpen(false)} patientId={id} onPredictionSaved={fetchPatientDetails}/>
    </Box>
  );
};

export default PatientDetails;