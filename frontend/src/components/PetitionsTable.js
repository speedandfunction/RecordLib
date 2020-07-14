import React from "react";
import { connect } from "react-redux";
import { PetitionConnected } from "./Petition";

export const PetitionsTable = (props) => {
  const { petitions = {} } = props;
  console.log("petitions");
  console.log(petitions);
  const { petitionCollection = {}, petitionUpdates = {} } = petitions;
  console.log("petitionCollection");
  console.log(petitionCollection);
  return (
    <div>
      {petitionCollection.petitionIds &&
      petitionCollection.petitionIds.length > 0 ? (
        petitionCollection.petitionIds.map((idx) => {
          return (
            <PetitionConnected key={idx} petitionId={idx}></PetitionConnected>
          );
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
