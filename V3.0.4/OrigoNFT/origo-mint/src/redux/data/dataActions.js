// log
import store from "../store";

const fetchDataRequest = () => {
  return {
    type: "CHECK_DATA_REQUEST",
  };
};

const fetchDataSuccess = (payload) => {
  return {
    type: "CHECK_DATA_SUCCESS",
    payload: payload,
  };
};

const fetchDataFailed = (payload) => {
  return {
    type: "CHECK_DATA_FAILED",
    payload: payload,
  };
};

export const fetchData = () => {
  return async (dispatch) => {
    dispatch(fetchDataRequest());
    try {
      let totalSupply = await store
        .getState()
        .blockchain.smartContract.methods.totalSupply()
        .call();
      
      let sale_state = await store
        .getState()
        .blockchain.smartContract.methods.sale_state()
        .call();  
        console.log("got sale state! ", sale_state);

      let pre_sale_cost = await store
        .getState()
        .blockchain.smartContract.methods.pre_sale_cost()
        .call();

      let public_sale_cost = await store
        .getState()
        .blockchain.smartContract.methods.public_sale_cost()
        .call();    

      dispatch(
        fetchDataSuccess({
          totalSupply,
          sale_state,
          pre_sale_cost,
          public_sale_cost,
        })
      );
    } catch (err) {
      console.log(err);
      console.log("error");
      dispatch(fetchDataFailed("Could not load data from contract."));
    }
  };
};
