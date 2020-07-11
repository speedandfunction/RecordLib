import React from "react";
import { connect } from "react-redux";

export const PetitionsTable = (props) => {
  const { petitions = {} } = props;
  const { petitionCollection = [], petitionUpdates = {} } = petitions;

  return (
    <div>
      {petitionCollection.length > 0 ? (
        petitionCollection.map((petition, idx) => {
          return <Petition key={idx} petition={petition}></Petition>;
        })
      ) : (
        <p>
          There are no petitions to display yet. Have you conducted an analysis
          yet?
        </p>
      )}
    </div>
  );
};

const mapStateToProps = (state) => {
  return {
    petitions: state.petitions,
  };
};

export const PetitionsTableConnected = connect(mapStateToProps)(PetitionsTable);
