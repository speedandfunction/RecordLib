import React from "react";
import CSSBaseline from "@material-ui/core/CssBaseline";
import Navbar from "./components/Navbar";
import About from "./components/About";
import UserProfile from "./components/UserProfile";
import NotFound from "./components/NotFound";
import PetitionProcess from "./components/PetitionProcess"
import { BrowserRouter as Router, Switch, Route, Redirect } from "react-router-dom";
import GettingStarted from "./components/GettingStarted";
import RecordUploader from "./components/RecordUploader";
import RecordEdit from "./components/RecordEdit";
import DownloadPetitions from "./components/DownloadPetitions";
import Analysis from "./components/Analysis";

function App() {
    return (<main className="content" style={{ margin: '0px'}}>
        <React.Fragment>
            <CSSBaseline/>
            <Router>
                <Navbar></Navbar>
                <Switch>
                    <Route path="/about">
                        <About/>
                    </Route>
                    <Route path="/profile">
                        <UserProfile/>
                    </Route>
                    <Route path="/applicant">
                        <GettingStarted/>
                    </Route>
                    <Route path="/sourcerecords">
                        <RecordUploader/>
                    </Route>
                    <Route path="/criminalrecord">
                        <RecordEdit/>
                    </Route>
                    <Route path="/analysis">
                        <Analysis/>    
                    </Route>
                    <Route path="/petitions">
                        <DownloadPetitions/>
                    </Route>
                    <Route path="/">
                        <Redirect to="/applicant"/>
                    </Route>
                    <Route path="">
                        <Redirect to="/applicant"/>
                    </Route>
                    <Route>
                        <NotFound/>
                    </Route>
                </Switch>
            </Router>



        </React.Fragment>
    </main>);
};

export default App;
